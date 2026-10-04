  if(#vec == 0, print("Vector ", vec_name, " is empty"); return);
  my(sorted_vec = vecsort(vec));
  my(v1 = sorted_vec[floor(n/3)]);
  my(v2 = sorted_vec[floor(2*n/3)]);
  print(vec_name, " tertiles: ", v1, " and ", v2);
  
  my(bin1_indices = select(i -> vec[i] < v1, [1..n]));
  my(logmass_bin1 = vector(#bin1_indices, j, logmass[bin1_indices[j]]));
  my(filtered_bin1 = filter_IQR(logmass_bin1));
  my(K_bin1 = compute_K_theory(filtered_bin1));
  print("K_theory for ", vec_name, " < ", v1, ": ", K_bin1);
  my(kurtosis_bin1 = compute_kurtosis(logmass_bin1));
  print("Kurtosis for ", vec_name, " < ", v1, ": ", kurtosis_bin1);
  
  my(bin2_indices = select(i -> vec[i] >= v1 && vec[i] < v2, [1..n]));
  my(logmass_bin2 = vector(#bin2_indices, j, logmass[bin2_indices[j]]));
  my(filtered_bin2 = filter_IQR(logmass_bin2));
  my(K_bin2 = compute_K_theory(filtered_bin2));
  print("K_theory for ", v1, " <= ", vec_name, " < ", v2, ": ", K_bin2);
  my(kurtosis_bin2 = compute_kurtosis(logmass_bin2));
  print("Kurtosis for ", v1, " <= ", vec_name, " < ", v2, ": ", kurtosis_bin2);
  
  my(bin3_indices = select(i -> vec[i] >= v2, [1..n]));
  my(logmass_bin3 = vector(#bin3_indices, j, logmass[bin3_indices[j]]));
  my(filtered_bin3 = filter_IQR(logmass_bin3));
  my(K_bin3 = compute_K_theory(filtered_bin3));
  print("K_theory for ", vec_name, " >= ", v2, ": ", K_bin3);
  my(kurtosis_bin3 = compute_kurtosis(logmass_bin3));
  print("Kurtosis for ", vec_name, " >= ", v2, ": ", kurtosis_bin3);
