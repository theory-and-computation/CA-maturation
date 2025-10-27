#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <map>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>
#include <typeinfo>

using namespace std;

//-----------------------------------------------------------------------------
// Helper Functions

void read_pot (string win_pot, int ndims, double x[], double k[]) {

  ifstream ifs (win_pot.c_str());
  string line;
  int i = 0;

  while (getline(ifs, line)) {
    istringstream iss(line);
    iss >> x[i];
    iss >> k[i];
    i++;     
  }
}

vector<int> compute_bin (int ndims, double x[], 
                         double xmin_array[], double dx_array[]) {

  vector<int> bin_position(ndims, 0);

  // Calculate bin position
  for (int i = 0; i < ndims; i++) {
    bin_position[i] = int( (x[i] - xmin_array[i]) / dx_array[i] ) + 1;        
  }

  return bin_position;
}

void bin_window (string tseries, const int nsteps, const int iwin, 
                 const int ndims, double xmin_array[], double dx_array[],
                 map<vector<int>, int> &histo_map) {

  ifstream ifs (tseries.c_str());
  string line;
  double time;
  double val[ndims]; // An array to store the read values.

  vector<int> bin_position (ndims, 0);
  map<vector<int>, int>::iterator map_iter;   // Map iterator

  double aveX[ndims];
  double rmsX[ndims];

  // Read the file line by line:
  while (getline(ifs,line)) {
    istringstream iss(line); 
    iss >> time;

    for (int j = 0; j < ndims; j++) {

      iss >> val[j];

      aveX[j] = aveX[j] + val[j];
      rmsX[j] = rmsX[j] + val[j] * val[j];
    }
    
    // Bin the data and store in a map:
    bin_position = compute_bin(ndims, val, xmin_array, dx_array);
    map_iter = histo_map.find(bin_position);

    if (map_iter == histo_map.end()) {   // No such bin existed, insert.
      histo_map.insert(map_iter, pair<vector<int>, int>(bin_position, 1));
    }
    else {                               // Existing bin, Increment count.
      histo_map[bin_position] = histo_map[bin_position] + 1;
    }
  }

  for (int j = 0; j < ndims; j++) {
    aveX[j] = aveX[j] / nsteps;
    rmsX[j] = rmsX[j] / nsteps;
    rmsX[j] = sqrt(abs(rmsX[j] - aveX[j] * aveX[j])); // Incorrect
  }

  // Print out averages 
  cout << "Last Timestep = " << time << endl; 
  for (int j = 0; j < ndims; j++) {
    cout << "Average X"<< j << " = " << aveX[j] << "    rms X" 
                       << j << " = " << rmsX[j] << endl;
  }
}

//-----------------------------------------------------------------------------

int main () {

  /*===========================================================================
   * Part 1 - Input and Output operations
   */

  string line;
  int ndims;

  ifstream infile ("wham-cc.inp");

  // Biased Distribution
  getline(infile, line);
  ofstream bia_file (line.c_str());
  cout << "Output Files" << endl;
  cout << "Total sampling, biased distribution: " << line << endl;

  // Unbiased Distribution
  getline(infile, line);
  ofstream rho_file (line.c_str());
  cout << "Unbiased distribution: " << line << endl;

  // PMF
  getline(infile, line);
  ofstream pmf_file (line.c_str());
  cout << "Free energy map: " << line << endl;

  // Get the dimensions and allocate xmin, xmax, and dx arrays
  getline(infile, line);
  istringstream iss (line);
  iss >> ndims;
  cout << "Number of Dimensions: " << ndims << "\n" << endl;

  // Allocate xmin, xmax, and dx arrays
  double xmin_array[ndims];
  double xmax_array[ndims];
  double dx_array[ndims];

  // Read the xmin, xmax and dx arrays
  getline(infile, line);
  ifstream xminfile (line.c_str());

  getline(infile, line);
  ifstream xmaxfile (line.c_str());

  getline(infile, line);
  ifstream dxfile (line.c_str());

  for (int i = 0; i < ndims; i++) {

    string xmin, xmax, dx;

    getline(xminfile, xmin);
    istringstream issxmin (xmin);

    getline(xmaxfile, xmax);
    istringstream issxmax (xmax);

    getline(dxfile, dx);
    istringstream issdx (dx);

    issxmin >> xmin_array[i];
    issxmax >> xmax_array[i];
    issdx >> dx_array[i];
  }

  xminfile.close();
  xmaxfile.close();
  dxfile.close();
  
  // CHECK 
  for (int i = 0; i < int(sizeof(xmax_array)/sizeof(*xmax_array)); i++ ) {
    cout << "First Position in Histogram of Variable " << i + 1 << ": " 
         << xmin_array[i] << endl;
    cout << "Last Position in Histogram of Variable  " << i + 1 << ": " 
         << xmax_array[i] << endl;
    cout << "Width of bins:                             " 
         << dx_array[i] << endl;
    cout << "Number of bins:  \n " << endl;
  }
  

  // Skip Eref, Xref
  getline(infile, line);

  // Read Tolerance and IterMax
  double tol;
  int iter_max;

  getline(infile, line);
  istringstream iter_control (line);
  iter_control >> tol;
  iter_control >> iter_max;

  cout << "Tolerance for WHAM iterations:       " << tol << endl;
  cout << "Maximum number of iterations:        " << iter_max << endl;

  // Read number of windows (Nwin)
  int nwin;

  getline(infile, line);

  istringstream Nwin (line);
  Nwin >> nwin;
  
  cout << "Total number of windows:              " << nwin << endl;

  /*===========================================================================
   * Part 2 - Read time series simulation data and initial analaysis
   */

  cout << "-----------------------------------------------------------" << endl;
  cout << "\nReading time-series:                                   \n" << endl;

  string Tseries[nwin];     // Filename containing the simulation data
  string win_pot[nwin];     // Filename containing the window potential 

  int nsteps[nwin];

  // Initialize window positions and force constants
  double x[nwin][ndims];
  double k[nwin][ndims];
  
  map<vector<int>,int> histo_map;  // Initialize bin map
  
  for (int i = 0; i < nwin; i++) { 

    getline (infile, Tseries[i]);
    cout << Tseries[i] << endl;
    getline (infile, win_pot[i]);
    cout << win_pot[i] << endl;
    
    getline (infile, line);
    nsteps[i] = atoi(line.c_str());
    cout << "Number of data in the histogram    " << nsteps[i] << endl;
    
    // Read and process the data: 
    read_pot(win_pot[i], ndims, x[i], k[i]);

    int iwin = i + 1;
    bin_window(Tseries[i], nsteps[i], iwin, ndims, xmin_array, dx_array,
               histo_map);

    cout << "Histogram size is " << histo_map.size() << endl;
    cout << endl;
  }

  // Set histogram array from map:
  int nbins = histo_map.size();
  int ncols = ndims + 1;

  int *histo = new int[nbins * ncols]();  // Allocate histogram array:

  map<vector<int>,int>::iterator mitr;
  
  int bin_n = 0;

  for (mitr = histo_map.begin(); mitr != histo_map.end(); ++mitr) {
    vector<int> v = mitr -> first;
    int count = mitr -> second;    
    
    for (int j = 0; j < ncols; j++) {
      if (j < ndims)
        histo[bin_n * ncols + j] = v[j];
      else
        histo[bin_n * ncols + j] = count;
    }
    bin_n++; 
  }

  // call destructor on hist_map:

  // Write the biased distribution file: 
  for (int i = 0; i < nbins; i++) {
    for (int j = 0; j < ncols; j++) {
      
      if (j < ndims) {
        int bin_ind = histo[i * ncols + j];
        bia_file << xmin_array[j] + bin_ind * dx_array[j] - dx_array[j] / 2
               << " ";
      }
      else
        bia_file << " " << histo[i * ncols + j] << endl; 
    }
  }
  
  /*===========================================================================
   * Part 3 - Iterate WHAM equations to unbias and recombine the histograms
   */

  cout << "Iterating WHAM.... " << endl;

  bool conv = false;
  int icycle = 0;

  // Allocate memory for free energy constants for each window.
  double *F  = new double[nwin](); 
  double *Fb = new double[nwin](); 
 
  // Boltzmann Temperature
  double kBoltz = 0.0019872;
  double Temp = 298.15;
  double kBT = kBoltz * Temp;
  
  double eps = 0.00000000001;
   
  double *rho = new double[nbins]();   // Map of unbiased distributions

  // Allocate memory for difference and Potential arrays:
  double *V = new double[nwin]();
  double *xb_array = new double[ndims]();
  double *dxb_array = new double[ndims]();

  while ((icycle < iter_max) & !conv) {

    // Set Fb to zero
    for (int iwin = 0; iwin < nwin; iwin++) {
      Fb[iwin] = 0;
    }

    for (int i = 0; i < nbins; i++) {          // Iterate over the bins
    
      // Compute the bin position from the bin indices    
      for (int j = 0; j < ndims; j++) {
        int bin = histo[i * ncols + j];
        xb_array[j] = xmin_array[j] + bin * dx_array[j] - dx_array[j] / 2;
      }

      // Compute rho (unbiased distribution) in WHAM equations
      int top = histo[i* ncols + ndims];        // Numerator of rho 
      double bot = 0;                           // Denominator of rho

      for (int iwin = 0; iwin < nwin; iwin++) { // Set Potential to zero
        V[iwin] = 0;
      }  
    
      for (int iwin = 0; iwin < nwin; iwin++) {

        // Get distance from bin to window potential
        for (int j = 0; j < ndims; j++) {
          dxb_array[j] = abs( xb_array[j] - x[iwin][j] );
          V[iwin] = 0.5 * k[iwin][j] * dxb_array[j] * dxb_array[j] + V[iwin];
        }
        bot =  bot + nsteps[iwin] * exp(( F[iwin] - V[iwin] ) / kBT);
      }

      if (bot > eps) { rho[i] = double(top / bot); }
      else { rho[i] = 0; }

      // Calculate the Fb
      for (int iwin = 0; iwin < nwin; iwin++) {
        Fb[iwin] = Fb[iwin] + rho[i] * exp( -V[iwin] / kBT );
      }
      
      /*      //Print out bin, densities
      cout.precision(10);
      cout << "Bin is : ";
      for (int j = 0; j < ncols; j++) {
        cout << histo[i * ncols + j]<< " ";
      }
      cout << "\nDensity is: " << rho[i] << endl;
      cout << "Top is: " << top << endl;
      cout << "Bot is: " << bot << endl;
      cout << "Fb is: \n";
      for (int j = 0; j < nwin; j++) {
        cout << Fb[j] << endl;
      }
      cout << endl;

    }
      */ 
    // Test for convergence:
    bool conv_check = true;

    for (int i = 0; i < nwin; i++) {
      double diff;
      Fb[i] = -kBT * log( Fb[i] );
      diff = abs( Fb[i] - F[i] - Fb[0] + F[0] );

      if ( diff > tol) {
        conv_check = false;
      }

      F[i] = Fb[i];
    } 
    conv = conv_check;
    icycle += 1;
  }

  cout << "Done! Number of iterations: " << icycle << endl << endl;

  // CHECK
  for (int i = 0; i < nwin; i++) {
    cout << "The converged F in window " << i << " = " << F[i] - F[0] << endl;
  }
  cout << endl;

  /*===========================================================================
   * Part 4 - Calculate the PMF from the unbiased distributions
   */

  // Grab the maximum of the unbiased distribution:
  double rhoMax = 0.0;
  int rhoMax_ind = 0;

  for (int i = 0; i < nbins; i++) {
    if (rho[i] > rhoMax) {
      rhoMax = rho[i];
      rhoMax_ind = i;
    }
  }

  cout << "Maximum density at:\n";
  for (int j = 0; j < ndims; j++) {

    // Get bin position
    int bin = histo[ rhoMax_ind * ncols + j];
    double xbin = xmin_array[j] + bin * dx_array[j] - (dx_array[j] / 2);

    cout << " X" << j << " = " << xbin << endl;
  }
  cout << endl;

  double *pmf = new double[nbins]();
  for (int i = 0; i < nbins; i++) {
    pmf[i] = -kBT * log( rho[i] / rhoMax );
  }

  double pmfMax = pmf[0];
  for (int i = 0; i < nbins; i++) {
    if (pmf[i] > pmfMax) { pmfMax = pmf[i]; }
  }

  cout << "Maximum free energy set to: " << pmfMax << " kcal/mol" << endl;

  for (int i = 0; i < nbins; i++) {
    // Compute the bin position from the bin indices
    double xb_array[ndims];
    
    for (int j = 0; j < ndims; j++) {
      int bin = histo[i * ncols + j];
      xb_array[j] = xmin_array[j] + bin * dx_array[j] - dx_array[j] / 2;
      
      rho_file << xb_array[j] << "  ";
      pmf_file << xb_array[j] << "  ";
    }

    rho_file << rho[i] / rhoMax << endl;
    pmf_file << pmf[i] << endl;
  }

}
