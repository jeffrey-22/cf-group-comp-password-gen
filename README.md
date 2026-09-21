## How to use:

I like to create a text file named `tokens.txt`, for storing secrets. These files should be secrets.

Create your contest on CF Gym Mashup. Then, you can see its URL (e.g. https://codeforces.com/gym/691856). Read and save the contest id (691856). 

Run `python3 gen_token.py`. This will generate a random token. Store it alongside the contest in `tokens.txt`, and keep it secret. Whenever you generate passwords, use this token as one of the input parameters, so that your generated passwords are deterministic. For example, let's say that token is `12345678`. You can put this token alongside the contest info in `tokens.txt`.

Create a text file named `team_name.txt` in this directory.

Fill that text file with names, one name per line, empty lines for placeholders.

Run `python3 gen.py team_name.txt <contest_id> <random_contest_token>`. For example, `python3 gen.py team_name.txt 691856 12345678`.

Optionally, append `> output.txt` to the following command to have it write to the `output.txt` file. So `python3 gen.py team_name.txt 691856 12345678 > output.txt`.

Now you have two files: `passwords.html` and `output.txt`. First file can be opened with browser and be used to print credentials. Second file contains text that you should copy over to codeforces: in https://codeforces.com/groups/my, open your group. Then, at the right sidebar, you can find "Manage domain users", and under it a button "Domain users". Open it, then copy the text in output.txt to the end of the textbox. Now these users have been registered to the corresponding contest in codeforces.

You can hand tweak `gen.py` to modify placeholder team names or name replacing structures. If you got an error running `gen.py`, chances are that there's some issues with name replacing. (for example, two teams have same name and stuff).