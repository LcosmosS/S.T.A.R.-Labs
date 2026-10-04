          git config user.name "github-actions[bot]"
            git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
            
            GIT_DIR=$REPO_ROOT/.git git --git-dir=$REPO_ROOT/.git --work-tree=$REPO_ROOT add "$output"
            
            if GIT_DIR=$REPO_ROOT/.git git --git-dir=$REPO_ROOT/.git --work-tree=$REPO_ROOT diff --staged --quiet; then
              echo "No changes for $base"
            else
