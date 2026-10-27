name: Profile activity

on:
  schedule:
    - cron: "17 */6 * * *"   # every 6 hours
  workflow_dispatch:          # lets you run it by hand from the Actions tab
  push:
    branches: [main]
    paths:
      - ".github/workflows/profile-activity.yml"
      - ".github/scripts/recent_activity.py"

permissions:
  contents: write

jobs:
  contribution-grid:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Generate contribution grid with snake
        uses: Platane/snk@v3
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/contribution-grid.svg?color_snake=#7aa2f7&color_dots=#ebedf0,#c7d2fe,#a5b4fc,#7aa2f7,#4f46e5
            dist/contribution-grid-dark.svg?palette=github-dark&color_snake=#bb9af7&color_dots=#161b22,#2b3a67,#3d59a1,#7aa2f7,#bb9af7

      - name: Publish SVGs to the output branch
        uses: crazy-max/ghaction-github-pages@v4
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  recent-activity:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4

      - name: Update Recent Activity section
        run: python3 .github/scripts/recent_activity.py
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GH_USER: ${{ github.repository_owner }}
          MAX_LINES: "6"

      - name: Commit if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add README.md
          git diff --cached --quiet || (git commit -m "Update recent activity" && git push)
