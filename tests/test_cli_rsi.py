from src.main import main


def test_cli_rsi_output(capsys):
    """Test CLI with RSI flag displays RSI value."""
    rc = main(["AAPL", "--rsi"])
    assert rc == 0
    captured = capsys.readouterr()
    out_lines = [line.strip() for line in captured.out.strip().splitlines() if line.strip()]

    assert out_lines[0].startswith("Close:")
    assert out_lines[1].startswith("Average:")
    assert out_lines[2].startswith("RSI (14):")


def test_cli_bands_and_rsi(capsys):
    """Test CLI with both bands and RSI flags."""
    rc = main(["AAPL", "--bands", "--rsi"])
    assert rc == 0
    captured = capsys.readouterr()
    out_lines = [line.strip() for line in captured.out.strip().splitlines() if line.strip()]

    assert out_lines[0].startswith("Close:")
    assert out_lines[1].startswith("Average:")
    assert out_lines[2].startswith("Lower Band:")
    assert out_lines[3].startswith("Upper Band:")
    assert out_lines[4].startswith("RSI (14):")
