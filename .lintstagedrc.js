// .lintstagedrc.js
module.exports = {
    'api/**/*.py': (absolutePaths) => {
        const cwd = process.cwd()
        const arguments = {
            args: absolutePaths,
            flake_args: absolutePaths.filter((fn) =>
                fn.match(RegExp(`/api/(focus_api|tests|bin)/`))
            ),
            mypy_args: absolutePaths.filter((fn) =>
                fn.match(RegExp(`/api/(focus_api|bin)/`))
            ),
        }
        const args = Object.keys(arguments)
            .map((key) =>
                !(arguments[key] && arguments[key].length)
                    ? undefined
                    : `${key}="${arguments[key].join(' ')}"`
            )
            .filter(Boolean)
            .join(' ')
        return [`cd ./api && make pre-commit ${args} `]
    },
    'api/openapi.yaml': ['cd ./api && make lint-spectral'],
}
