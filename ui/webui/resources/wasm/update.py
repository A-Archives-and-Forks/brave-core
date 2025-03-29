#!/usr/bin/env vpython3
# Copyright (c) 2025 The Brave Authors. All rights reserved.
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at https://mozilla.org/MPL/2.0/.

# update.py vendors the deps of the Rust workspace in `wasm`.
# Run this script via npm run update_wasm_resources
# whenever you need to add a new workspace member,
# or bump the version of an existing member's deps.

import os
from pathlib import Path
import shutil
import subprocess
import sys
import toml

import brave_chromium_utils

with brave_chromium_utils.sys_path('//tools/rust'):
    import update_rust
    CARGO = os.path.join(update_rust.RUST_TOOLCHAIN_OUT_DIR, 'bin',
                         'cargo' + ('.exe' if sys.platform == 'win32' else ''))

CONFIG_TOML = {
    'source': {
        'crates-io': {
            'replace-with': 'vendored-sources'
        },
        'vendored-sources': {
            'directory': '../vendor'
        }
    }
}


def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    members = toml.load('Cargo.toml')['workspace']['members']

    shutil.rmtree('vendor', ignore_errors=True)
    for member in members:
        Path(f'{member}/.cargo/config.toml').unlink(missing_ok=True)

    subprocess.run([CARGO, 'vendor'], check=True)
    for member in members:
        Path(f'{member}/.cargo').mkdir(exist_ok=True)
        with open(Path(f'{member}/.cargo/config.toml'), 'w') as f:
            toml.dump(CONFIG_TOML, f)


if __name__ == '__main__':
    main()
