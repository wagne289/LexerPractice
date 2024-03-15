from Gobbledegook import interpret_gobbledegook

def test_test001(capsys):
    inp = """
    start;
        consolesays 5;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""5
"""


def test_test002(capsys):
    inp = """
    start;
        if 1 == 1 start;
            consolesays "tautology";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""tautology
"""

def test_test003(capsys):
    inp = """
    start;
        if 1 == 1
        start;
            consolesays "tautology";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""tautology
"""


def test_test004(capsys):
    inp = """
    start;
        nvar a = 1;
        if a == 1 start;
            consolesays "indeed";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()
    assert captured.out == r"""indeed
"""


def test_test005(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a == b start;
            consolesays "two variables are equal";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""two variables are equal
"""


def test_test006(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a == b start;
            consolesays "two variables are equal";
        end; else start;
            consolesays "two variables are not the same";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""two variables are equal
"""


def test_test007(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a == b start; consolesays "two variables are equal"; end;
        else start; consolesays "two variables are not the same"; end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""two variables are equal
"""

def test_test008(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a != b start;
            consolesays "topsy";
        end; else start;
            consolesays "turvy";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""turvy
"""


def test_test009(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a > b start;
            consolesays "topsy";
        end; else start;
            consolesays "turvy";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""turvy
"""


def test_test010(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a >= b start;
            consolesays "topsy";
        end; else start;
            consolesays "turvy";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""topsy
"""


def test_test011(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a <= b start;
            consolesays "topsy";
        end; else start;
            consolesays "turvy";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""topsy
"""

def test_test012(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a < b start;
            consolesays "topsy";
        end; else start;
            consolesays "turvy";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""turvy
"""


def test_test013(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a < b + 1 start;
            consolesays "topsy";
        end; else start;
            consolesays "turvy";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""topsy
"""


def test_test014(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a + 2 < b + 1 start;
            consolesays "topsy";
        end; else start;
            consolesays "turvy";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""turvy
"""


def test_test015(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a == 1 and b == 1 start;
            consolesays "topsy";
        end; else start;
            consolesays "turvy";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""topsy
"""

def test_test016(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a == 1 and b != 1 start;
            consolesays "topsy";
        end; else start;
            consolesays "turvy";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""turvy
"""

def test_test017(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a == 1 or b != 1 start;
            consolesays "topsy";
        end; else start;
            consolesays "turvy";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""topsy
"""

def test_test018(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a == 1 or b != 1 start;
            consolesays "topsy";
            if 7 == 7 start;
                consolesays "nest";
            end;
        end; else start;
            consolesays "turvy";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""topsy
nest
"""

def test_test019(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a == 1 or b != 1 start;
            consolesays "topsy";
            if 7 == 8 start;
                consolesays "nest";
            end; else start;
                consolesays "alternest";
            end;
        end; else start;
            consolesays "turvy";
        end;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""topsy
alternest
"""

def test_test020(capsys):
    inp = """
    start;
        nvar a = 1;
        nvar b = 1;
        if a == 1 or b != 1 start;
            consolesays "topsy";
            if 7 == 8 start;
                consolesays "nest";
            end; else start;
                consolesays "alternest";
                a = 6;
            end;
        end; else start;
            consolesays "turvy";
        end;

        consolesays a;
    end;
    """

    interpret_gobbledegook(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""topsy
alternest
6
"""