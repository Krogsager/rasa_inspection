The CLI tool inspector.py to scan your domain, nlu and actions files for consistency, and helps you keep your files aligned.
Place inspector.py in your rasa project folder.

# Run

`python inspector.py --story data/stories.md --domain domain.yml  --nlu nlu/nlu_danish.md`

or update the default args file paths.

# Limitations

* currently does not work with custom actions
* currently does not work with emojis


