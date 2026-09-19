#!/usr/bin/env bats
#
# $ bats tests/git-ssh.bats

setup() {
  GIT_SSH_BIN="${BATS_TEST_DIRNAME}/../git-ssh"

  export HOME="${BATS_TEST_TMPDIR}/home"
  mkdir -p "${HOME}"
  export XDG_CONFIG_HOME="${BATS_TEST_TMPDIR}/config"

  KEY_DIR="${BATS_TEST_TMPDIR}/keys"
  mkdir -p "${KEY_DIR}"
  KEY_PATH="${KEY_DIR}/id_test"
  printf 'fake-private-key\n' >"${KEY_PATH}"

  CONFIG_DIR="${XDG_CONFIG_HOME}/git-ssh"
}

@test "version prints the version and exits 0" {
  run "${GIT_SSH_BIN}" version
  [ "${status}" -eq 0 ]
  [[ "${output}" == *"[git-ssh]:"* ]]
}

@test "no arguments prints usage and exits 0" {
  run "${GIT_SSH_BIN}"
  [ "${status}" -eq 0 ]
  [[ "${output}" == *"[Commands]"* ]]
}

@test "unknown command prints usage and exits 1" {
  run "${GIT_SSH_BIN}" bogus
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"[Commands]"* ]]
}

@test "create requires a config name" {
  run "${GIT_SSH_BIN}" create
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"Missing config name"* ]]
}

@test "create requires a key path" {
  run "${GIT_SSH_BIN}" create myconf
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"Missing config path"* ]]
}

@test "create rejects a config name containing a slash" {
  run "${GIT_SSH_BIN}" create "../evil" "${KEY_PATH}"
  [ "${status}" -eq 1 ]
  [[ "${output}" == *'must not contain "/"'* ]]
  [ ! -d "${XDG_CONFIG_HOME}/evil.2" ]
}

@test "create fails when the key file does not exist" {
  run "${GIT_SSH_BIN}" create myconf "${KEY_DIR}/does-not-exist"
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"does not exist"* ]]
}

@test "create refuses to overwrite an existing config" {
  "${GIT_SSH_BIN}" create myconf "${KEY_PATH}"
  run "${GIT_SSH_BIN}" create myconf "${KEY_PATH}"
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"already exists"* ]]
}

@test "create writes a 0600 config file inside a 0700 config directory" {
  run "${GIT_SSH_BIN}" create myconf "${KEY_PATH}"
  [ "${status}" -eq 0 ]

  config_file="${CONFIG_DIR}/myconf.2"
  [ -e "${config_file}" ]
  [ "$(stat -c '%a' "${CONFIG_DIR}")" = "700" ]
  [ "$(stat -c '%a' "${config_file}")" = "600" ]
}

@test "create preserves a key path containing spaces" {
  spaced_key="${KEY_DIR}/my key"
  printf 'fake-private-key\n' >"${spaced_key}"

  run "${GIT_SSH_BIN}" create spaced "${spaced_key}"
  [ "${status}" -eq 0 ]

  grep -qF "IdentityFile ${spaced_key}" "${CONFIG_DIR}/spaced.2"
}

@test "delete requires a config name" {
  run "${GIT_SSH_BIN}" delete
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"Missing config name"* ]]
}

@test "delete rejects a config name containing a slash" {
  run "${GIT_SSH_BIN}" delete "../../etc/passwd"
  [ "${status}" -eq 1 ]
  [[ "${output}" == *'must not contain "/"'* ]]
}

@test "delete fails for a config that does not exist" {
  run "${GIT_SSH_BIN}" delete nope
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"does not exist"* ]]
}

@test "delete removes an existing config" {
  "${GIT_SSH_BIN}" create myconf "${KEY_PATH}"
  run "${GIT_SSH_BIN}" delete myconf
  [ "${status}" -eq 0 ]
  [ ! -e "${CONFIG_DIR}/myconf.2" ]
}

@test "list prints nothing but succeeds when no configs exist" {
  run "${GIT_SSH_BIN}" list
  [ "${status}" -eq 0 ]
}

@test "list shows a created config" {
  "${GIT_SSH_BIN}" create myconf "${KEY_PATH}"
  run "${GIT_SSH_BIN}" list
  [ "${status}" -eq 0 ]
  [[ "${output}" == *"myconf.2"* ]]
}

@test "list --verbose dumps the config file contents" {
  "${GIT_SSH_BIN}" create myconf "${KEY_PATH}"
  run "${GIT_SSH_BIN}" list --verbose
  [ "${status}" -eq 0 ]
  [[ "${output}" == *"IdentityFile ${KEY_PATH}"* ]]
}

@test "export fails for a config that does not exist" {
  run "${GIT_SSH_BIN}" export nope
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"Missing config"* ]]
}

@test "export rejects a config name containing a slash" {
  run "${GIT_SSH_BIN}" export "../../etc/passwd"
  [ "${status}" -eq 1 ]
  [[ "${output}" == *'must not contain "/"'* ]]
}

@test "export prints a GIT_SSH_COMMAND for an existing config" {
  "${GIT_SSH_BIN}" create myconf "${KEY_PATH}"
  run "${GIT_SSH_BIN}" export myconf
  [ "${status}" -eq 0 ]
  [[ "${output}" == *"export GIT_SSH_COMMAND="* ]]
  [[ "${output}" == *"myconf.2"* ]]
}

@test "reset prints commands to unset GIT_SSH_COMMAND" {
  run "${GIT_SSH_BIN}" reset
  [ "${status}" -eq 0 ]
  [[ "${output}" == *"unset GIT_SSH_COMMAND"* ]]
}
