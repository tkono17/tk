{
char libname[100] = "lib/";
cout << "Generating HTML files ..." << endl;
gSystem->Load(libname);
THtml html;
html.SetSourceDir(".:./inc:./src");
html.SetOutputDir("/raid/kohno/WWW/physics/mvd/tools/htmldoc");
html.MakeAll();
html.MakeIndex();
cout << "" << endl;
}
