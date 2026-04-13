from pathlib import Path
import sys
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.ingestion import Ingestion


def test_run_cicflowmeter_uncomments_exe_cmd_args(tmp_path, monkeypatch):
    cic_root = tmp_path / "CICFlowMeter"
    cic_root.mkdir()
    gradlew = cic_root / "gradlew"
    gradlew.write_text("#!/bin/sh\n")

    build_gradle = cic_root / "build.gradle"
    original_build = '\n'.join(
        [
            "task exeCMD(type: JavaExec){",
            "    main = \"cic.cs.unb.ca.ifm.Cmd\"",
            "    //args = [\"/tmp/in\", \"/tmp/out\"]",
            "}",
        ]
    )
    build_gradle.write_text(original_build)

    pcap_day_dir = tmp_path / "pcaps"
    pcap_day_dir.mkdir()
    pcap_file = pcap_day_dir / "capture.pcap"
    pcap_file.write_bytes(b"pcap")

    csv_day_dir = tmp_path / "csv"
    csv_day_dir.mkdir()

    ingestion = Ingestion.__new__(Ingestion)
    ingestion.cic_root = cic_root

    monkeypatch.setattr(ingestion, "_make_gradle_env", lambda: {})

    def fake_run(command, cwd, env):
        patched_build = build_gradle.read_text()
        expected_line = f'args = ["{pcap_file}", "{csv_day_dir / pcap_file.stem}"]'

        assert expected_line in patched_build
        assert f"//{expected_line}" not in patched_build
        assert command == [str(gradlew), "--no-daemon", "exeCMD"]
        assert cwd == str(cic_root)
        assert env == {}
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr("core.ingestion.subprocess.run", fake_run)

    ingestion._run_cicflowmeter(pcap_day_dir, csv_day_dir)

    assert build_gradle.read_text() == original_build