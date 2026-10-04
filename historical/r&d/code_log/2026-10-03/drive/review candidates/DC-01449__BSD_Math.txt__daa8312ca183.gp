  if(#v == 0, return(0));
  v = vecsort(v);
  n = #v;
  if(n % 2 == 1, v[(n+1)/2], (v[n/2] + v[n/2 + 1]) / 2)
}
%1046 = (v)->if(#v==0,return(0));v=vecsort(v);n=#v;if(n%2==1,v[(n+1)/2],(v[n/2]+v[n/2+1])/2)
