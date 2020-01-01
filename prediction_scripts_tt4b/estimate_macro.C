{
binnum=39;
h1=ttHH4b->GetBinContent(binnum);
h2=ttbb->GetBinContent(binnum);
h3=tt2b->GetBinContent(binnum);
h4=ttb->GetBinContent(binnum);
h5=ttcc->GetBinContent(binnum);
h6=ttlf->GetBinContent(binnum);
hsum=h2+h3+h4+h5+h6;
cout << "sum of singal  in the last bin is: " << h1 << endl;
cout << "sum of background in the last bin is: " << hsum << endl;
sig_sqrtb= h1/(sqrt(hsum));
cout << "sig/sqrt(b) = " << sig_sqrtb << endl;
}
