#!/usr/bin/env zsh

cat<<EOF

 Git workflow in Athena

0. Setup
setupATLAS
lsetup git

1. Git clone and remote setup
Clone my fork repository and set the atlas/athena.git as the upstream repository.
git clone https://:@gitlab.cern.ch:8443/tkohno/athena.git
cd athena
git remote add upstream https://:@gitlab.cern.ch:8443/atlas/athena.git
git remove -v

2. Work with a branch
Synchronize with the upstream repository and checkout the branch.
git fetch upstream
git checkout -b master-branch upstream/master --no-track

3. Local commit
git add -A (or specify each file)
git status
git commit -m 'some comment'
git log --oneline <path/to/package>
git show <commitId>
git push --set-upstream origin master-branch

4. Merge request

5. Resolve conflict
git fetch upstream
git merge upstream/master

EOF
