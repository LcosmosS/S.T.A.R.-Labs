  print("K_theory for ", vec_name, " < ", v1, ": ", K_bin1);
  print("Kurtosis for ", vec_name, " < ", v1, ": ", kurtosis_bin1);


  my(K_bin2 = compute_K_theory(bin2));
  my(kurtosis_bin2 = compute_kurtosis(bin2));
  print("K_theory for ", v1, " <= ", vec_name, " < ", v2, ": ", K_bin2);
  print("Kurtosis for ", v1, " <= ", vec_name, " < ", v2, ": ", kurtosis_bin2);


  my(K_bin3 = compute_K_theory(bin3));
  my(kurtosis_bin3 = compute_kurtosis(bin3));
  print("K_theory for ", vec_name, " >= ", v2, ": ", K_bin3);
  print("Kurtosis for ", vec_name, " >= ", v2, ": ", kurtosis_bin3);
}
