        # nbconvert / IPython sometimes tries to write to an unwritable parent.
        # Force a writable IPYTHONDIR and ensure permissions.
        export IPYTHONDIR=/tmp/.ipython
        mkdir -p "$IPYTHONDIR"
        chmod -R 0777 "$IPYTHONDIR"
        # Export for subsequent steps in this job
        echo "IPYTHONDIR=$IPYTHONDIR" >> $GITHUB_ENV
    
    - name: Clone arithmetic archives
      run: |
