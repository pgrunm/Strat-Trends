# Errbot Based Chatbot for postmortems

## Installation

1. Clone the repo.
2. Create a virtual Python3 environment and install the requirements with `pip install -r requiments.txt`.
3. Initialize the errbot with `errbot --init` in the root directory.

### Preparing the plugin development

```bash
errbot -–new-plugin
```

## Plugin documentation

- [ErrBot Plugin Development](https://errbot.readthedocs.io/en/latest/user_guide/plugin_development/development_environment.html#)
- [ErrBot Plugin Testing](https://errbot.readthedocs.io/en/latest/user_guide/plugin_development/testing.html)

## How to Errbot

### Args

The command /example abc def gives you `abc` and `def` as list in args.

### Markdown templates

See the [Errbot docs](https://errbot.readthedocs.io/en/latest/user_guide/plugin_development/messaging.html#templating) for more information on how to use templates.