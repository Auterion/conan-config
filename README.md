# Conan Configurations

This repo holds the [Conan](https://conan.io/) configurations used within Auterion.
To install it, first make sure you have conan version 2 installed.
Then it is only a simple:

```bash
conan config install git@github.com:Auterion/conan-config.git
```

## Customizing

The default profile used in this configuration is `x86_64-linux-relwithdebinfo-gcc9`.
If you want to use a different profile, you can either specify it during the `conan build` step (read `conan build -h` for more info).
The other option is to change the `~/.conan2/profiles/default` symbolic link to point to the profile you want to use by default.
