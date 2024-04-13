//  file: diffeq_pendulum.cpp
//
//  Program to solve the differential equation for a physical
//   (chaotic) pendulum, as in Chapter 14 of the Landau/Paez text
//
//  Programmer:  Dick Furnstahl  furnstahl.1@osu.edu
//               Connor Fricke   fricke.59@osu.edu
//
//  Revision history:
//      02/10/04  original version, translated from diffeq_pendulum.c
//      02/17/04  including direct piping to gnuplot (from gnuplot_i.c)
//      01/30/06  put declarations and initializations together;
//                 switched to <cmath>
//      02/05/06  switched to GnuplotPipe class
//      04/03/24  adapted to VisualizingChaos Project for Physics 5810 Final Project.
//                Cleaned up main(), restructured IO, added plot_params struct and 
//                queryParameters() function.
//      04/05/24  Attempted to include both Bash + Pwsh functionality
//  Notes:
//   * Based on the discussion of differential equations in Chap. 9
//      of "Computational Physics" by Landau and Paez and of
//      differential chaos in phase space in Chap. 14.
//   * Uses the fourth-order Runge-Kutta ode routine (equal step)
//   * Angular position is theta(t) and angular velocity is theta_dot(t)
//   * We've added _ext to the driving force (for "external")
//
//******************************************************************
// include files
#define _USE_MATH_DEFINES // for M_PI definition
#include <iostream>
#include <iomanip>        
#include <fstream>        
#include <string>
#include <cstdlib>
using namespace std; 
#include <cmath>
#include "diffeq_routines.h" // diffeq routine prototypes
#include "GnuplotPipe.h"     // direct piping

// STRINGS FOR THINGS
string OS;    
string CLEAR_CMD;         // derived from OS
string GNUPLOT_TERMINAL;  // derived from OS

// ************************** structures ***************************
// DEFAULT PARAMETERS FOR PENDULUM
struct pendulum_parameters
{
  double omega0 = 1.0;      // natural frequency
  double alpha = 0.2;       // coefficient of friction
  double f_ext = 0.2;       // amplitude of external force
  double omega_ext = 0.689; // frequency of external force
  double phi_ext = 0.0;     // phase angle for external force
  double theta0 = 0.8;      // initial (angular) position
  double theta_dot0 = 0.0;  // initial (angular) velocity
  double T_ext = 2. * M_PI / omega_ext; // period for external frequency
};

// DEFAULT PARAMETERS USED FOR PLOTTING
struct plot_parameters
{
  int T_skip = 1000;      // every T_skip points means once every T_ext
  double tmin = 0.;       // starting t value
  double tmax = 50.;      // last t value
  double plot_min = tmin; // first t value to plot
  double plot_max = tmax; // last t value to plot
  int plot_skip = 10;     // plot every plot_skip points
  int plot_delay = 10;    // wait plot_delay msec between points
};

// ************************** func prototypes ***************************
double rhs(double t, double y[], int i, void *params_ptr);
void queryParameters(pendulum_parameters &pendParams, plot_parameters &plotParams, double &h);

// ************************** main program ***************************
int main(void)
{
  // *** OS NEEDED FOR SOME FEATURES TO WORK ***
  cout << "Enter OS (windows / linux):\n>> ";
  cin >> OS;

  if (OS == "Windows" or OS == "windows")
  {
    GNUPLOT_TERMINAL = "windows";
    CLEAR_CMD = "cls";
  }
  else if (OS == "Linux" or OS == "linux")
  {
    GNUPLOT_TERMINAL = "x11";
    CLEAR_CMD = "clear";
  }
  else
  {
    // shouldn't get here
    cout << "Error, invalid OS. Terminating Program.\n";
    return EXIT_FAILURE;
  }

  // *** INITIALIZE ***
  const string FILENAME = "datafiles/diffeq_pendulum.dat"; // filename for the output file
  GnuplotPipe myPipe;

  const int N = 2; // 2nd order equation --> 2 coupled 1st
  double y_rk4[N]; // vector of y functions

  void *rhs_params_ptr;           // void pointer for rhs()
  pendulum_parameters pendParams; // parameters for the pendulum behavior
  plot_parameters plotParams;     // parameters for Gnuplot behavior
  double h;                       // parameter for diffeq routine

  // START OF MENU FUNCTIONALITY
  repeat:
  {
    // this function handles the menu prompting and assigning values entered by the user
    queryParameters(pendParams, plotParams, h);

    rhs_params_ptr = &pendParams; // load void pointer for rhs()

    // *** PLOTTING STAGE ***
    // set some properties of the Gnuplot Pipe
    myPipe.set_terminal(GNUPLOT_TERMINAL + " title 'Gnuplot: Visualizing Chaos' size 720,720");
    myPipe.set_title("Pendulum Phase Space");
    myPipe.set_xlabel("theta");
    myPipe.set_ylabel("theta dot");
    myPipe.set_delay(1000 * plotParams.plot_delay); // set_delay in usec
    cout << "Plotting now (wait until complete) . . ." << endl;

    // open the output file
    ofstream out; // declare the output file
    out.open(FILENAME, ofstream::trunc);

    myPipe.init(); // start up piping to gnuplot

    y_rk4[0] = pendParams.theta0;     // initial condition for y0(t)
    y_rk4[1] = pendParams.theta_dot0; // initial condition for y1(t)

    // print out the parameters, a header, and the first set of points
    out << "# omega0=" << pendParams.omega0 << ", alpha=" << pendParams.alpha << endl;
    out << "# theta0=" << pendParams.theta0 << ", theta_dot0=" << pendParams.theta_dot0 << endl;
    out << "# t_start=" << plotParams.tmin << ", t_end=" << plotParams.tmax << ", h="
        << h << endl;
    out << "#   t          theta(t)                 thetadot(t)       " << endl;

    if (plotParams.tmin >= plotParams.plot_min)
    {
      out << plotParams.tmin << " " << scientific << setprecision(15)
          << y_rk4[0] << " " << y_rk4[1] << endl;
      myPipe.plot(pendParams.theta0, pendParams.theta_dot0);  // plot 1st point
      myPipe.plot2(pendParams.theta0, pendParams.theta_dot0); // plot 1st point
    }

    int point_count = 0; // initialize point counter
    for (double t = plotParams.tmin; t <= plotParams.tmax; t += h)
    {
      // find y(t+h) by a 4th order Runge-Kutta step
      runge4(N, t, y_rk4, h, rhs, rhs_params_ptr);

      if ((t >= plotParams.plot_min) & (t <= plotParams.plot_max))
      {
        point_count++; // increment point counter

        double theta = y_rk4[0];     // current angle
        double theta_dot = y_rk4[1]; // current angular velocity

        if ((point_count % plotParams.plot_skip) == 0)
        { // plot every plot_skip points
          out << t + h << " " << scientific << setprecision(15)
              << theta << " " << theta_dot << endl;
          // send points to gnuplot
          myPipe.plot(theta, theta_dot);
        }
        if ((point_count % plotParams.T_skip) == 0)
        { // plot every T_skip points
          // send points to gnuplot
          myPipe.plot2(theta, theta_dot);
        }
      }
    } // end for loop over t

    out << endl;
    out.close(); // close the output file
    cout << "\n results added to datafiles/diffeq_pendulum.dat\n\n";
  }
  // allow the user to run the program again if they choose
  char AGAIN;
  cout << "Again? Y/N\n>> ";
  cin >> AGAIN;
  if (AGAIN == 'Y' or AGAIN == 'y')
    goto repeat;

  cout << "Wait while the pipe is closed . . . " << flush;
  myPipe.finish(); // close the pipe to gnuplot
  cout << "Complete." << endl;

  return EXIT_SUCCESS; // successful completion!
}

//*************************** rhs ***************************
//
//  * This is the function defining the i'th right hand side of
//     the diffential equations:
//             dy[i]/dt = rhs(t,y[],i)
//  * We take this from eqs. (14.5) through (14.7) in Landau/Paez
//
//*************************************************************
double
rhs(double t, double y[], int i, void *params_ptr)
{
  // define local force parameters from passed structure
  double omega0 = ((pendulum_parameters *)params_ptr)->omega0;
  double alpha = ((pendulum_parameters *)params_ptr)->alpha;
  double f_ext = ((pendulum_parameters *)params_ptr)->f_ext;
  double omega_ext = ((pendulum_parameters *)params_ptr)->omega_ext;
  double phi_ext = ((pendulum_parameters *)params_ptr)->phi_ext;

  // External force
  double F_ext = f_ext * cos(omega_ext * t + phi_ext);

  if (i == 0)
  {
    return (y[1]);
  }

  if (i == 1)
  {
    return (-omega0 * omega0 * sin(y[0]) - alpha * y[1] + F_ext);
  }

  return (1); // something's wrong if we get here
}

//******************* queryParameters *************************
//
//  * Originally part of main() function, moved to a separate
//    task for readability. This function takes pass-by-reference
//    parameters, most of which are stored between two structs.
//  * The function reprompts the user for a value they'd like to
//    change until they enter 0.
//  * T_ext and h do not belong to either struct because they are
//    calculated using values from the structs, though they could
//    be added to the structs optionally
//
//*************************************************************
void queryParameters(pendulum_parameters &pendParams, plot_parameters &plotParams, double &h)
{
  // modify and return extraneous parameters that do not belong to either structure
  h = pendParams.T_ext / double(plotParams.T_skip);

  // PROMPT FOR ALL OTHER PARAMETERS
  int answer = 1;     // answer to parameter queries
  while (answer != 0) // iterate until told to move on
  {
    int CLEARED = system(CLEAR_CMD.c_str());  // clear terminal before showing menu
    if (CLEARED)
    {
      cout << "Error using clear command.\n";
    }
    // MENU OPTIONS:
    cout << "\nCurrent parameters:\n";
    cout << "[1] omega0 = " << pendParams.omega0 << endl;
    cout << "[2] alpha = " << pendParams.alpha << endl;
    cout << "[3] f_ext = " << pendParams.f_ext << endl;
    cout << "[4] w_ext = " << pendParams.omega_ext << endl;
    cout << "[5] phi_ext = " << pendParams.phi_ext << endl;
    cout << "[6] theta0 = " << pendParams.theta0 << endl;
    cout << "[7] theta_dot0 = " << pendParams.theta_dot0 << endl;
    cout << "[8] t_start = " << plotParams.tmin << endl;
    cout << "[9] t_end = " << plotParams.tmax << endl;
    cout << "[10] h = " << h << endl;
    cout << "[11] plot_start = " << plotParams.plot_min << endl;
    cout << "[12] plot_end = " << plotParams.plot_max << endl;
    cout << "[13] plot_skip = " << plotParams.plot_skip << endl;
    cout << "[14] Gnuplot_delay = " << plotParams.plot_delay << endl;
    cout << "\nWhat do you want to change? [0 for none] ";

    cin >> answer;
    cout << endl;

    switch (answer)
    {
    case 0:
      break;
    case 1:
      cout << "enter omega0:\n>> ";
      cin >> pendParams.omega0;
      break;
    case 2:
      cout << "enter alpha:\n>> ";
      cin >> pendParams.alpha;
      break;
    case 3:
      cout << "enter f_ext:\n>> ";
      cin >> pendParams.f_ext;
      break;
    case 4:
      cout << "enter w_ext:\n>> ";
      cin >> pendParams.omega_ext;
      pendParams.T_ext = 2. * M_PI / pendParams.omega_ext;
      h = pendParams.T_ext / 1000.; // set h according to external period
      break;
    case 5:
      cout << "enter phi_ext:\n>> ";
      cin >> pendParams.phi_ext;
      break;
    case 6:
      cout << "enter theta0:\n>> ";
      cin >> pendParams.theta0;
      break;
    case 7:
      cout << "enter theta_dot0:\n>> ";
      cin >> pendParams.theta_dot0;
      break;
    case 8:
      cout << "enter t_start:\n>> ";
      cin >> plotParams.tmin;
      break;
    case 9:
      cout << "enter t_end:\n>> ";
      cin >> plotParams.tmax;
      break;
    case 10:
      cout << "enter h:\n>> ";
      cin >> h;
      break;
    case 11:
      cout << "enter plot_start:\n>> ";
      cin >> plotParams.plot_min;
      break;
    case 12:
      cout << "enter plot_end:\n>> ";
      cin >> plotParams.plot_max;
      break;
    case 13:
      cout << "enter plot_skip:\n>> ";
      cin >> plotParams.plot_skip;
      break;
    case 14:
      cout << "enter Gnuplot_delay (in msec):\n>> ";
      cin >> plotParams.plot_delay;

    default:
      break;
    } // end switch answer
  }   // end answer while

  return;
}