import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

class Transform:
    # Coordinate file import
    def import_known(self, known_file):
        self.known_coords = np.loadtxt(known_file)
    def import_observed(self, observed_file):
        self.observed_coords = np.loadtxt(observed_file)

     # Transformation switch
    def transform(self, transform_type):
        if transform_type == "s":
            self.type = "s"
            self.similarity()
        elif transform_type == "a":
            self.type = "a"
            self.affine()
        elif transform_type == "p":
            self.type = "p"
            self.projective()

    # Transformation adjustments
    def similarity(self):
        # Prep some variables common to all transformations
        self.adjustment_prep()
        # A matrix
        A = np.zeros((self.num_points*2, 4))
        for i in range(self.num_points):
            A[2*i,0] = self.xc[i]
            A[2*i,1] = -self.yc[i]
            A[2*i,2] = 1
            A[2*i,3] = 0
            A[2*i+1,0] = self.yc[i]
            A[2*i+1,1] = self.xc[i]
            A[2*i+1,2] = 0
            A[2*i+1,3] = 1
        # Least squares estimate of unknowns
        x_hat = np.linalg.inv(A.T.dot(A)).dot(A.T).dot(self.l_vec)
        # Residuals
        self.residuals = np.squeeze(A.dot(x_hat) - self.l_vec)
        # Linear parameters
        a = x_hat.item(0)
        b = x_hat.item(1)
        t_x = x_hat.item(2)
        t_y = x_hat.item(3)
        self.linear_params = (a, b, t_x, t_y)
        # Nonlinear parameters
        scale = np.sqrt(a**2 + b**2)
        rotation = np.rad2deg(np.arctan(b/a))
        self.nonlinear_params = (scale, rotation)
    def affine(self):
        # Prep some variables common to all transformations
        self.adjustment_prep()
        # A matrix
        A = np.zeros((self.num_points*2, 6))
        for i in range(self.num_points):
            A[2*i,0] = self.xc[i]
            A[2*i,1] = self.yc[i]
            A[2*i,2] = 1
            A[2*i,3] = 0
            A[2*i,4] = 0
            A[2*i,5] = 0
            A[2*i+1,0] = 0
            A[2*i+1,1] = 0
            A[2*i+1,2] = 0
            A[2*i+1,3] = self.xc[i]
            A[2*i+1,4] = self.yc[i]
            A[2*i+1,5] = 1
        # Least squares estimate of unknowns
        x_hat = np.linalg.inv(A.T.dot(A)).dot(A.T).dot(self.l_vec)
        # Residuals
        self.residuals = np.squeeze(A.dot(x_hat) - self.l_vec)
        # Linear parameters
        a = x_hat.item(0)
        b = x_hat.item(1)
        t_x = x_hat.item(2)
        c = x_hat.item(3)
        d = x_hat.item(4)
        t_y = x_hat.item(5)
        self.linear_params = (a, b, c, d, t_x, t_y)
        # Nonlinear parameters
        scale_x = np.sqrt(a**2 + c**2)
        scale_y = np.sqrt(b**2 + d**2)
        rotation = np.rad2deg(np.arctan(b/a))
        non_orthog = np.rad2deg(np.arctan((a*b+c*d)/(a*d-b*c)))
        self.nonlinear_params = (scale_x, scale_y, rotation, non_orthog)
    def projective(self):
         # Prep some variables common to all transformations
        self.adjustment_prep()
        # A matrix
        A = np.zeros((self.num_points*2, 8))
        for i in range(self.num_points):
            A[2*i,0] = self.xc[i]
            A[2*i,1] = self.yc[i]
            A[2*i,2] = 1
            A[2*i,3] = 0
            A[2*i,4] = 0
            A[2*i,5] = 0
            A[2*i,6] = -self.xc[i]*self.xf[i]
            A[2*i,7] = -self.yc[i]*self.xf[i]
            A[2*i+1,0] = 0
            A[2*i+1,1] = 0
            A[2*i+1,2] = 0
            A[2*i+1,3] = self.xc[i]
            A[2*i+1,4] = self.yc[i]
            A[2*i+1,5] = 1
            A[2*i+1,6] = -self.xc[i]*self.yf[i]
            A[2*i+1,7] = -self.yc[i]*self.yf[i]
        # Least squares estimate of unknowns
        x_hat = np.linalg.inv(A.T.dot(A)).dot(A.T).dot(self.l_vec)
        # Residuals
        self.residuals = np.squeeze(A.dot(x_hat) - self.l_vec)
        # Linear parameters
        a1 = x_hat.item(0)
        a2 = x_hat.item(1)
        a3 = x_hat.item(2) # t_x
        b1 = x_hat.item(3)
        b2 = x_hat.item(4)
        b3 = x_hat.item(5) # t_y
        c1 = x_hat.item(6) # plane equation x coefficient
        c2 = x_hat.item(7) # plane equation y coefficient
        self.linear_params = (a1, a2, a3, b1, b2, b3, c1, c2)
        # Nonlinear parameters
        scale_x = np.sqrt(a1**2 + b1**2) # a1 = a, b1 = c in affine
        scale_y = np.sqrt(a2**2 + b2**2) # a2 = b, b2 = d in affine
        rotation = np.rad2deg(np.arctan(a2/a1))
        non_orthog = np.rad2deg(np.arctan((a1*a2+b1*b2)/(a1*b2-a2*b1)))
        self.nonlinear_params = (scale_x, scale_y, rotation, non_orthog)

    def adjustment_prep(self):
        # Sort by point numbers for clean output at the end
        self.known_coords = self.known_coords[
            self.known_coords[:,0].argsort()]
        self.observed_coords = self.observed_coords[
            self.observed_coords[:,0].argsort()]
        # Store point numbers for ease of later output
        self.point_nums = self.known_coords[:,0]
        # Fiducial coords
        self.xf = self.known_coords[:,1]
        self.yf = self.known_coords[:,2]
        # Comparator coords
        self.xc = self.observed_coords[:,1]
        self.yc = self.observed_coords[:,2]
        # Number of points
        self.num_points = self.known_coords.shape[0]
        # Observation vector of fiducial coordinates
        self.l_vec = np.reshape(np.stack((self.xf, self.yf), axis=-1),
            (self.num_points*2, 1))

    # Formatted result output
    def print_results(self):
        if self.type == "s":
            print("------------------------------------")
            print("SIMILARITY TRANSFORMATION ADJUSTMENT")
            print("------------------------------------")
        elif self.type == "a":
            print("--------------------------------")
            print("AFFINE TRANSFORMATION ADJUSTMENT")
            print("--------------------------------")
        elif self.type == "p":
            print("------------------------------------")
            print("PROJECTIVE TRANSFORMATION ADJUSTMENT")
            print("------------------------------------")

        print("LINEAR PARAMETERS")
        if self.type == "s":
            print("a = {:.10f}".format(self.linear_params[0]))
            print("b = {:.10f}".format(self.linear_params[1]))
            print("delta x = {:.4f} mm".format(self.linear_params[2]))
            print("delta y = {:.4f} mm".format(self.linear_params[3]))
        elif self.type == "a":
            print("a = {:.10f}".format(self.linear_params[0]))
            print("b = {:.10f}".format(self.linear_params[1]))
            print("c = {:.10f}".format(self.linear_params[2]))
            print("d = {:.10f}".format(self.linear_params[3]))
            print("delta x = {:.4f} mm".format(self.linear_params[4]))
            print("delta y = {:.4f} mm".format(self.linear_params[5]))
        elif self.type == "p":
            print("a1 = {:.10f} (affine a)".format(self.linear_params[0]))
            print("a2 = {:.10f} (affine b)".format(self.linear_params[1]))
            print("a3 = {:.10f} (delta x)".format(self.linear_params[2]))
            print("b1 = {:.10f} (affine c)".format(self.linear_params[3]))
            print("b2 = {:.10f} (affine d)".format(self.linear_params[4]))
            print("b3 = {:.10f} (delta y)".format(self.linear_params[5]))
            print("c1 = {:.10f} (plane x coefficient)".format(self.linear_params[6]))
            print("c2 = {:.10f} (plane y coefficnet)".format(self.linear_params[7]))

        print("\nNON-LINEAR PARAMETERS")
        if self.type == "s":
            print("scale = {:.8f}".format(self.nonlinear_params[0]))
            print("rotation = {:.4f} degrees".format(self.nonlinear_params[1]))
        elif self.type == "a":
            print("scale x = {:.8f}".format(self.nonlinear_params[0]))
            print("scale y = {:.8f}".format(self.nonlinear_params[1]))
            print("rotation = {:.4f} degrees".format(self.nonlinear_params[2]))
            print("non-orthogonality = {:.4f} degrees".format(self.nonlinear_params[3]))
        elif self.type == "p":
            print("scale x = {:.8f}".format(self.nonlinear_params[0]))
            print("scale y = {:.8f}".format(self.nonlinear_params[1]))
            print("rotation = {:.4f} degrees".format(self.nonlinear_params[2]))
            print("non-orthogonality = {:.4f} degrees".format(self.nonlinear_params[3]))
        
        print("\nCOORDINATES AND RESIDUALS IN FIDUCIAL SYSTEM (UNITS=mm)")
        residual_table = np.stack((self.point_nums, self.xf,
            self.residuals[::2], self.yf, self.residuals[1::2])).T
        headers = ["#", "x", "x residual", "y", "y residual"]
        print(tabulate(residual_table, headers, tablefmt="simple",
            floatfmt=(".0f", ".3f", ".4f", ".3f", ".4f")))
        
        print("\nROOT MEAN SQUARE ERRORS")
        print("RMSE x = {:.4f} mm".format(
            np.sqrt(np.square(self.residuals[::2]).mean())))
        print("RMSE y = {:.4f} mm".format(
            np.sqrt(np.square(self.residuals[1::2]).mean())))

    # Plot generation
    def show_quiver(self):
        scale = 0.0005
        plt.quiver(self.xf, self.yf, self.residuals[::2], self.residuals[1::2],
            angles="xy", scale_units="xy", scale=scale)
        plt.axis("equal")
        plt.xlabel("X Fiducial (mm)")
        plt.ylabel("Y Fiducial (mm)")
        if self.type == "s":
            plt.title("Similarity Transformation Adjustment")
        elif self.type == "a":
            plt.title("Affine Transformation Adjustment Residuals")
        elif self.type == "p":
            plt.title("Projective Transformation Adjustment Residuals")
        scale_factor = "Scale Factor = 1:{:.0f}".format(1/scale)
        plt.text(0, 0, scale_factor, horizontalalignment="center",
            verticalalignment="center")
        plt.show()
