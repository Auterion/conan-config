# Conan Configurations

This repo holds the [Conan](https://conan.io/) configurations used within Auterion.
To install it, first make sure you have conan version 2 installed.
Then it is only a simple:

```bash
conan config install git@github.com:Auterion/conan-config.git
```

## Customizing

The default profile used is `x86_64-linux-relwithdebinfo-gcc9`.
If you want to use a different profile, you can either specify it during the `conan build` step (read `conan build -h` for more info) or set it as the default profile by changing the `~/.conan2/profiles/default` symbolic link.

## Generating the profiles

The creation of the profiles is handled through the `render_profiles.py` script.
To generate the profiles, run:

```bash
pipenv run python render_profiles.py
```

If `pipenv` is not installed, you can install it with:

```bash
pip install pipenv
```

### Modifying the profiles

The profiles are generated from the associated `*.jinja` files in the `templates` directory.
The `render_profiles.py` script will render the templates and place the resulting profiles in the `profiles` directory.
So if you want to modify the profiles, you should modify the templates and then re-run the `render_profiles.py` script.
