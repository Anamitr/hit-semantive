import re
import subprocess


def test_example_from_mail(test_dir):
    """ Uses installed hit, not local repository files """
    script = "hit init\n" \
             "touch file1 && touch file2\n" \
             "hit status\n" \
             "hit add file1 && hit status\n" \
             "hit commit && hit status\n" \
             "echo 'test' >> file1 && hit status\n" \
             "hit add file1 && hit commit && hit status\n" \
             "hit add * && hit commit && hit status\n"
    completed_process = subprocess.run(script, shell=True,
                                       stdout=subprocess.PIPE)
    out = completed_process.stdout.decode()

    assert re.match("Initialized empty Hit repository in [/\w-]+.hit",
                    out.split('\n')[0])

    all_out_but_first_line = "\n".join(out.split('\n')[1:])
    expected_out_but_first_line = '> file1 (new file)\n> file2 (new file)\n' \
                                  '> file1 (staged file)\n> file2 (new file)\n' \
                                  '> file2 (new file)\n> file1 (modified file)\n' \
                                  '> file2 (new file)\n> file2 (new file)\n> \n'
    assert all_out_but_first_line == expected_out_but_first_line
