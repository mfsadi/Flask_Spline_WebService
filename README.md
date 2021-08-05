# Flask Spline Web Service
In this project, an image is uploaded into a web service and a spline is drawn on top of
it using three basic spline parameters, namely t, c and k. The spline is drawn using Scipy
and Matplotlib libraries.

In mathematics, a spline is a special function defined piecewise by polynomials. In
interpolating problems, spline interpolation is often preferred to polynomial interpolation
because it yields similar results, even when using low-degree polynomials, while avoiding
Runge’s phenomenon for higher degrees (Wikipedia).

We used a combination of Matplotlib and Scipy libraries to load an image, make spline based on the given parameters and draw
spline on top of the image. The details of implementation is provided in the next section.
The web service is built using Flask framework. In this service a simple HTML form is
provided to receive users’ inputs such as image and parameters. Then, these inputs will be
sent to the specific functions to compute the spline and then the final image which include
the spline curves will be shown to the user. The User Interface is fairly simple and easy to
use. Exceptions are caught and handled to some degrees and where this happens, a spline
is provided using default parameters.

Main libraries:

Flask 2.0.1

Flask-Bootstrap 3.3.7.1

Flask-Uploads 0.2.1

Flask-WTF 0.15.1

matplotlib 3.4.2

numpy 1.21.1

scipy 1.7.0
