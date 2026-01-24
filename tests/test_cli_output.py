from src.main import main


def test_cli_bands_output(capsys):
    # call CLI with bands to include lower and upper bands
    rc = main(["AAPL", "--bands"])
    assert rc == 0
    captured = capsys.readouterr()
    out_lines = [line.strip() for line in captured.out.strip().splitlines() if line.strip()]

    assert out_lines[0].startswith("Close:")
    assert out_lines[1].startswith("Average:")
    assert out_lines[2].startswith("Lower Band:")
    assert out_lines[3].startswith("Upper Band:")


def test_cli_default_output(capsys):
    # default output should include Close and Average only
    rc = main(["AAPL"])
    assert rc == 0
    captured = capsys.readouterr()
    out_lines = [line.strip() for line in captured.out.strip().splitlines() if line.strip()]

    assert out_lines[0].startswith("Close:")
    assert out_lines[1].startswith("Average:")
    assert len(out_lines) == 2
