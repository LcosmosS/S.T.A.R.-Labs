        sudo apt-get update
        sudo apt-get install -y python3 python3-pip
        pip3 install numpy pandas

    - name: Run regression diffs
      continue-on-error: true
      run: |
        mkdir -p diff_report
        python3 scripts/diff_outputs.py current/ previous/ diff_report/

    - name: Upload diff report
      uses: actions/upload-artifact@v4
