with open('masses.txt', 'w') as f:
    f.write('[' + ', '.join(map(str, masses)) + ']')
with open('redshifts.txt', 'w') as f:
   *     f.write('[' + ', '.join(map(str, df['z'])) + ']')
   * This will produce files like [123.456, 789.012, ...], which read() can interpret as a vector.
* Alternative: If you prefer not to change the files, use readstr() and parse the string in PARI/GP:
* pari
M_str = readstr("masses.txt");
* M = vector(length(M_str), i, eval(M_str[i]));
* However, adjusting the file format is simpler.
