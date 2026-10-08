"""Run real MongoDB integration tests without touching classroom data."""
import argparse
import os
import socket
import subprocess
import sys
import time
import uuid
from pathlib import Path

from pymongo import MongoClient
from pymongo.errors import PyMongoError


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mongod", required=True)
    parser.add_argument("--port", type=int, default=27107)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    if not 1 <= args.port <= 65535:
        parser.error("port must be 1..65535")
    runtime = root / "infra/runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    owned = runtime / ("day22-validation-" + uuid.uuid4().hex)
    owned.mkdir()
    assert owned.resolve().is_relative_to(runtime.resolve())
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", args.port))
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    uri = f"mongodb://127.0.0.1:{args.port}/?replicaSet=ads-sync-validation"
    log = (owned / "mongod.log").open("w", encoding="utf-8")
    server = subprocess.Popen([
        args.mongod, "--replSet", "ads-sync-validation", "--port", str(args.port),
        "--bind_ip", "127.0.0.1", "--dbpath", str(owned),
    ], stdout=log, stderr=subprocess.STDOUT, creationflags=flags)
    direct = MongoClient(f"mongodb://127.0.0.1:{args.port}/?directConnection=true",
                         serverSelectionTimeoutMS=500)
    try:
        for attempt in range(50):
            if server.poll() is not None:
                raise RuntimeError("Test MongoDB exited; inspect " + str(owned / "mongod.log"))
            try:
                direct.admin.command("ping")
                break
            except PyMongoError:
                time.sleep(0.15)
        else:
            raise RuntimeError("Test MongoDB did not respond")
        direct.admin.command("replSetInitiate", {
            "_id": "ads-sync-validation",
            "members": [{"_id": 0, "host": f"127.0.0.1:{args.port}"}],
        })
        for attempt in range(100):
            if direct.admin.command("hello").get("isWritablePrimary"):
                break
            time.sleep(0.15)
        else:
            raise RuntimeError("Test primary election did not finish")
        env = dict(os.environ, ADS_TEST_MONGO_URI=uri, PYTHONUTF8="1")
        result = subprocess.run([
            sys.executable, "-B", "ad_config/manage.py", "test", "ads", "--verbosity", "2",
        ], cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", creationflags=flags, timeout=120)
        print(result.stdout)
        if "Ran " not in result.stdout or "skipped=" in result.stdout:
            raise RuntimeError("The full integration suite did not execute")
        return result.returncode
    finally:
        if server.poll() is None:
            try:
                direct.admin.command("shutdown", force=True)
            except PyMongoError:
                pass
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.terminate()
                server.wait(timeout=5)
        direct.close()
        log.close()
        print("Isolated MongoDB stopped:", server.poll() is not None)
        print("Test logs:", owned.relative_to(root))


if __name__ == "__main__":
    raise SystemExit(main())
