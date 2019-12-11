# Housekeeping
This project is managed using Github's tools like Issues, Pull requests, and Projects.
## Issues https://github.com/mikaeilorfanian/pytest-visualize/issues
Every change to the project comes as result of an Issue.
## Pull requests https://github.com/mikaeilorfanian/pytest-visualize/pulls
Pull requests contain changes related to one or more issues.   
To distinguish the source of changes in the pull request, each commit has the following format:   
`<issue#>-<commit-type>-<summary>`   
"issue#" - Github Issue number - points to the Github Issue which will contain details about the reasons for the change.   
"commit-type" is for specific commits like "bug fix", "chores", "refactor", "cleaning up" which don't add extra functionality but are necessary for the health of the application.
### Special Commit Types
*bug fix* is a small bug fix, usually a couple of lines long. Bigger fixes must be done in a separate GitHub issue.   
*refactor*, same as bug fixes but for code improvements. Refactors DON'T change functionality.   
*cleanup* is usually for removing outdated never used code, formatting (e.g. fixing flake8 warnings), etc. Again, these don't change any functionality.   
*chores* are like clean ups which don't involve code or features. For example, updating the `README`s or `.gitignore`.   
*PRR* is a change related to a pull request review. It's basically a change requested or suggested by a reviewer.   
## Project https://github.com/mikaeilorfanian/pytest-visualize/projects/1
Using the link above, you can track progress on
- issues picked for implementation (To-do column)
- work in progress
- and finally issues which are "done"
## Definition of "done"
"done" here means that changes related to the issue have been merged with the master branch and can be used by end users.
