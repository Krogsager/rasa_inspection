The CLI tool inspector.py to scan your domain, nlu and actions files for consistency, and helps you keep your files aligned.
Place inspector.py in your rasa project folder.

# Run

`python inspector.py --story data/stories.md --domain domain.yml  --nlu nlu/nlu_danish.md`

or update the default args file paths.

Result:

![image](https://user-images.githubusercontent.com/27994384/47293318-19764b00-d60a-11e8-9bab-7e5ebbe67793.png)

# Limitations

* currently does not work with custom actions
* currently does not work with emojis


