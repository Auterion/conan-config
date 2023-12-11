#!/bin/env python3

from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import Any


"""
This script will render the profiles for the different platforms and compilers
that we support. It will also symlink the default profile to the one we want to
use by default.

The profiles are rendered from the templates in the jinja templates directory.
So if you want to change the profiles, you should change the templates instead.
"""

file_dir = Path(__file__).parent

# Path to templates
template_dir = file_dir / "templates"

# Path to profiles
profile_dir = file_dir / "profiles"

# Create the jinja2 environment
env = Environment(
    loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True
)


def render_template(template_name, **kwargs):
    # Load the template
    template = env.get_template(template_name)

    # Render the template
    return template.render(**kwargs)


def save_profile(profile, settings):
    os = settings["os"]["name"].lower()
    architecture = settings["architecture"]["name"].lower()
    compiler = (
        f"{settings['compiler']['name'].lower()}-{settings['compiler']['version']}"
    )
    build_type = settings["build_type"].lower()

    file_name = f"{architecture}-{os}-{build_type}-{compiler}"

    with open(profile_dir / file_name, "w") as f:
        f.write(profile)


def render_and_save_profile(settings):
    profile = (
        render_template(
            settings["os"]["name"].lower() + ".jinja",
            **settings,
        ).rstrip()
        + "\n"
    )

    save_profile(profile, settings)


def main():
    # Clean out the profiles directory
    print("Cleaning out profiles directory")
    for file in profile_dir.glob("*"):
        file.unlink()

    architectures = {
        "x86_64": {"name": "x86_64", "conan_name": "x86_64", "apple_name": "x86_64"},
        "aarch64": {"name": "aarch64", "conan_name": "armv8", "apple_name": "arm64"},
    }

    compilers = [
        {"name": "gcc", "version": "11"},
        {"name": "gcc", "version": "9"},
        {"name": "clang", "version": "14"},
    ]

    build_types = ["Debug", "RelWithDebInfo", "Release"]

    # Create linux profiles
    print("Creating linux profiles")
    settings: dict[str, Any] = {
        "os": {"name": "Linux", },
    }
    for architecture in architectures.values():
        for compiler in compilers:
            # Skip aarch64 clang, for now
            if architecture["name"] == "aarch64" and compiler["name"] == "clang":
                continue
            for build_type in build_types:
                settings["architecture"] = architecture
                settings["compiler"] = compiler
                settings["build_type"] = build_type

                render_and_save_profile(settings)

    # Create windows profiles
    print("Creating windows profiles")
    settings = {
        "os": {"name": "Windows", },
        "architecture": architectures["x86_64"],
        "compiler": {"name": "msvc", "version": "192", "runtime": "dynamic"},
    }
    for build_type in build_types:
        settings["build_type"] = build_type

        render_and_save_profile(settings)

    # Create android profiles
    print("Creating android profiles")
    settings = {
        "os": {"name": "Android", },
        "architecture": architectures["aarch64"],
        "compiler": {"name": "clang", "version": "14"},
    }
    for build_type in build_types:
        settings["build_type"] = build_type

        render_and_save_profile(settings)

    # Create macos profiles
    print("Creating macos profiles")
    settings = {
        "os": {"name": "Macos", "version": "11.0"},
        "architecture": architectures["x86_64"],
        "compiler": {"name": "apple-clang", "version": "14"},
    }
    for build_type in build_types:
        for architecture in architectures.values():
            settings["build_type"] = build_type
            settings["architecture"] = architecture

            render_and_save_profile(settings)

    # Set up the symlink for the default profile
    print("Setting up default profile")
    default_profile = profile_dir / "default"
    if default_profile.exists():
        default_profile.unlink()

    # The default profile is the x86_64-linux-release-gcc-9 profile
    default_profile.symlink_to("x86_64-linux-release-gcc-9")

    print("Done!")


if __name__ == "__main__":
    main()
