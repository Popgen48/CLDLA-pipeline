// A simple C++ program to perform bending (if negative eigenvalues encountered) to make the matrix positive using Schaeffer's method (https://animalbiosciences.uoguelph.ca/~lrs/ELARES/PDforce.pdf)

// Requires the Eigen library (https://eigen.tuxfamily.org/dox/GettingStarted.html)

#include <iostream>
#include <fstream>
#include <Eigen/Dense>

// Function to write a matrix to a text file
void writeMatrixToFile(const Eigen::MatrixXd &matrix, const std::string &filename)
{
    std::ofstream outfile(filename);
    if (!outfile)
    {
        std::cerr << "Failed to open the output file." << std::endl;
        return;
    }

    // Write the number of rows to the file
    // outfile << matrix.rows() << std::endl;

    // Write the matrix values to the file in the specified format
    for (int i = 0; i < matrix.rows(); ++i)
    {
        for (int j = 0; j < matrix.cols(); ++j)
        {
            outfile << i + 1 << " " << j + 1 << " " << matrix(i, j) << std::endl;
        }
    }

    // Close the output file
    outfile.close();
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        std::cerr << "Usage: " << argv[0] << " <input_file> <output_file>" << std::endl;
        return 1;
    }

    // Open the input file
    std::ifstream infile(argv[1]);

    if (!infile)
    {
        std::cerr << "Failed to open the input file." << argv[1] << std::endl;
        return 1;
    }

    int num_rows;
    infile >> num_rows;
    std::cout << "Matrix size: " << num_rows << "x" << num_rows << std::endl;

    // Create a dynamic matrix to hold the data
    Eigen::MatrixXd A(num_rows, num_rows);

    int row, col;
    double value;

    // Read matrix values from the file
    while (infile >> row >> col >> value)
    {
        A(row - 1, col - 1) = value;
    }

    // Close the input file
    infile.close();

    // Perform eigenvalue decomposition
    Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> eigensolver(A);

    if (eigensolver.info() != Eigen::Success)
    {
        std::cerr << "Eigenvalue decomposition failed." << std::endl;
        return 1;
    }

    // Get the eigenvalues
    Eigen::VectorXd eigenvalues = eigensolver.eigenvalues();

    // Sort the eigenvalues in descending order
    eigenvalues = eigenvalues.reverse();

    // Print the eigenvalues
    // std::cout << "Eigenvalues:" << std::endl;
    // std::cout << eigenvalues << std::endl;

    // Check for negative eigenvalues
    bool hasNegativeEigenvalues = eigenvalues.minCoeff() < 0;

    if (hasNegativeEigenvalues)
    {
        std::cout << "The matrix has negative eigenvalues. Proceeding to bending..." << std::endl;

        // Step 1: Calculate 's = (sum of all neg eigenvals) × 2'
        double s = (eigenvalues.array() < 0).cast<double>().sum() * 2.0;

        // Step 2: Calculate 't = (s × s) × 100 + 1'
        double t = (s - eigenvalues.minCoeff()) * (s - eigenvalues.minCoeff()) * 100.0 + 1.0;

        // Step 3: Replace negative eigenvalues (n's) using 'n_new = p × (s − n) × (s − n)/t' where p is the smallest positive eigenvalue
        eigenvalues = (eigenvalues.array() >= 0).select(eigenvalues, eigenvalues.minCoeff() * (s - eigenvalues.array()).square() / t);

        // Print the modified eigenvalues
        // std::cout << "Modified Eigenvalues:" << std::endl;
        // std::cout << eigenvalues << std::endl;

        // Create a new matrix using modified eigenvalues and original eigenvectors
        Eigen::MatrixXd B = eigensolver.eigenvectors() * eigenvalues.asDiagonal() * eigensolver.eigenvectors().transpose();

        // Print the new matrix B
        // std::cout << "Matrix B:" << std::endl;
        // std::cout << B << std::endl;

        // Save the new matrix B to a text file
        writeMatrixToFile(B, argv[2]);

        std::cout << "Matrix bending finished. Output saved to '" << argv[2] << "'" << std::endl;
    }
    else
    {
        std::cout << "No negative eigenvalues found. Matrix can be used as it is for inversion." << std::endl;

        std::ifstream infile(argv[1]);
        std::string firstLine;
        std::getline(infile, firstLine); // Read and discard the first line

        // Save the remaining data to a new file
        std::ofstream outfile(argv[2]);
        outfile << infile.rdbuf();
        outfile.close();

        std::cout << "Output saved to '" << argv[2] << "'" << std::endl;
    }

    return 0;
}
