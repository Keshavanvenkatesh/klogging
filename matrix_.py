import random
import math

class Matrix:
    def __init__(self, mat):
        self.matrix = mat
        self.no_of_rows = len(mat)
        self.no_of_columns = len(mat[0])

    @staticmethod
    def matrix(no_of_rows, no_of_columns):
        matrix = []
        for _ in range(no_of_rows):
            row = []
            while len(row) < no_of_columns:
                try:
                    element = int(input("enter element:"))
                    row.append(element)
                except:
                    print("ENTER ONLY NUMBERS!!!")
            matrix.append(row)
        return Matrix(matrix)

    def order(self):
        return f"{self.no_of_rows} X {self.no_of_columns}"
    
    def max_size_element(self):
        max_ = 1
        for i in range(self.no_of_rows):
            for j in range(self.no_of_columns):
                temp = len(str(self.matrix[i][j]))
                if temp > max_:
                    max_ = temp
        return max_
    
    def show(self, identity="Matrix"):
        max_ = self.max_size_element()
        print()
        if identity == "Matrix":
            print(f"{identity}:")
        else:
            print(f"{identity}=")

        for i in range(self.no_of_rows):
            print("|", end=" ")
            for j in range(self.no_of_columns):
                print(f"{self.matrix[i][j]:>{max_}}", end=" ")
            print("|")

# ======================================================= basic functions ======================================================

    def __add__(self, other):
        sum_matrix = []
        if self.order_check(other):
            for i in range(len(self.matrix)):
                sum_matrix.append(Matrix.row_sum(self.matrix[i], other.matrix[i]))
        return Matrix(sum_matrix)

    def __sub__(self, other):
        sub_matrix = []
        if self.order_check(other):
            for i in range(len(self.matrix)):
                sub_matrix.append(Matrix.row_sub(self.matrix[i], other.matrix[i]))
        return Matrix(sub_matrix)
    
    def __mul__(self, other):
        if isinstance(other, Matrix):
            if len(self.matrix[0]) == len(other.matrix):
                matrix = []
                temp_row = [[]]
                for j in range(len(other.matrix[0])):
                    for i in range(len(other.matrix)):
                        temp_row[j].append(other.matrix[i][j])
                    temp_row.append([])
                temp_row.pop()

                for i in range(len(self.matrix)):
                    temp = []
                    for j in range(len(temp_row)):
                        temp.append(Matrix.row_mul(self.matrix[i], temp_row[j]))
                    matrix.append(temp)
                return Matrix(matrix)
            else:
                print("cannot multiply these matrix")
                return f"cannot multiply these matrix"
            
        elif isinstance(other, (int, float)):
            matrix = []
            for i in range(len(self.matrix)):
                temp = []
                for j in range(len(self.matrix[0])):
                    temp.append(self.matrix[i][j] * other)
                matrix.append(temp)
            return Matrix(matrix)
        else:
            return NotImplemented
        
    def __rmul__(self, other):
        return self * other
    
    def __pow__(self, n):
        if not isinstance(n, int):
            raise TypeError("only integer allowed")

        if n < 0:
            return (self.inverse()) ** (-n)
        elif n == 0:
            # identity matrix
            matrix = []
            for i in range(self.no_of_rows):
                row = []
                for j in range(self.no_of_columns):
                    if i == j:
                        row.append(1)
                    else:
                        row.append(0)
                matrix.append(row)
            return Matrix(matrix)
        else:
            product = self
            for _ in range(n - 1):
                product = product * self
            return product

    def __eq__(self, other):

        if self.no_of_rows != other.no_of_rows or self.no_of_columns != other.no_of_columns:
            return False

        condition = True
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != other.matrix[i][j]:
                    condition = False
        return condition
    
    def __xor__(self, other):   # element wise  product
        if self.no_of_columns == other.no_of_columns and self.no_of_rows == other.no_of_rows:
            matrix = []
            for i in range(self.no_of_rows):
                row = []
                for j in range(self.no_of_columns):
                    row.append(self.matrix[i][j] * other.matrix[i][j])
                matrix.append(row)
            return Matrix(matrix)
        else:
            raise ValueError("not of equal order")
    
    def trace(self):
        if self.no_of_columns == self.no_of_rows:
            sum_ = 0
            for i in range(self.no_of_rows):
                sum_ += self.matrix[i][i]
            return sum_
        else:
            raise ValueError("Trace only defined for square matrices")

    def order_check(self, other):
        return (len(self.matrix) == len(other.matrix) 
                and len(self.matrix[0]) == len(other.matrix[0]))
    
    @staticmethod
    def row_sum(l1, l2):
        return [l1[i] + l2[i] for i in range(len(l1))]
    
    @staticmethod
    def row_sub(l1, l2):
        return [l1[i] - l2[i] for i in range(len(l1))]

    @staticmethod
    def row_mul(l1, l2):
        return sum(l1[i] * l2[i] for i in range(len(l1)))
    
# ======================================================= transpose ============================================================

    def transpose(self, type="modify"):
        t_matrix = []
        for i in range(len(self.matrix[0])):
            row = []
            for j in range(len(self.matrix)):
                row.append(self.matrix[j][i])
            t_matrix.append(row)

        if type == "new":
            return Matrix(t_matrix)
        elif type == "modify":
            self.matrix = t_matrix
            self.no_of_rows, self.no_of_columns = self.no_of_columns, self.no_of_rows
        else:
            print("not a valid type")
            return "not a valid type"

# ======================================================= determinant ============================================================

    def det(self):
        if self.no_of_rows != self.no_of_columns:
            print("Not a square matrix")
            return None

        def determinant(matrix):
            n = len(matrix)
            if n == 1:
                return matrix[0][0]
            if n == 2:
                return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
            det_val = 0
            for col in range(n):
                submatrix = [row[:col] + row[col+1:] for row in matrix[1:]]
                det_val += ((-1) ** col) * matrix[0][col] * determinant(submatrix)
            return det_val

        return determinant(self.matrix)

# ======================================================= adjoint / inverse / orthogonal ============================================================

    def adjoint(self):
        matrix = []
        for i in range(self.no_of_rows):
            row = []
            for j in range(self.no_of_columns):
                cofactor_ = Matrix.cofactor(i, j, self.matrix)
                row.append(cofactor_)
            matrix.append(row)
        return Matrix(matrix).transpose("new")
    
    def inverse(self):
        return (self.adjoint()) * (1 / self.det())

    @staticmethod
    def cofactor(m, n, matrix):
        row_count = len(matrix)
        column_count = len(matrix[0])

        if row_count != column_count:
            print("not a square matrix - cofactor")
            return None

        cofactor_matrix = []
        for i in range(row_count):
            if i == m:
                continue
            row = []
            for j in range(column_count):
                if j == n:
                    continue
                row.append(matrix[i][j])
            cofactor_matrix.append(row)

        bc = Matrix(cofactor_matrix)
        return bc.det() * ((-1) ** (m + n))

    def orthogonal_check(self, tol=1e-9):
        if self.no_of_rows != self.no_of_columns:
            return False
        product = self * self.transpose("new")
        identity = Matrix.identity_matrix(self.no_of_rows)
        
        for i in range(self.no_of_rows):
            for j in range(self.no_of_columns):
                if abs(product.matrix[i][j] - identity.matrix[i][j]) > tol:
                    return False
        return True


# ======================================================= random ============================================================

    @staticmethod
    def random(m, n, range_=(0, 10)):
        matrix = []
        for _ in range(m):
            row = []
            for _ in range(n):
                row.append(random.randint(range_[0], range_[1]))
            matrix.append(row)
        return Matrix(matrix)
    
# ======================================================= extras ============================================================

    @staticmethod
    def identity_matrix(n):
        matrix=[]
        for i in range(n):
            row=[]
            for j in range(n):
                if i == j:
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)
        return Matrix(matrix)

    def Frobenius_norm(self):
        square_sum=0
        for i in range(self.no_of_rows):
            for j in range(self.no_of_columns):
                square_sum+=(self.matrix[i][j])**2
        return math.sqrt(square_sum)
    
    def __str__(self):
        self.show()
        return ""
    
    def __repr__(self):
        return "m1=Matrix.matrix(m,n)"
    
    def help():
        msg = """
================ Matrix Class Help ================

Constructor:
  Matrix(list_of_lists)         -> Create a Matrix from nested lists

Static Generators:
  Matrix.matrix(m, n)           -> Create an m x n matrix from user input
  Matrix.random(m, n, (a,b))    -> Create an m x n random matrix with values in [a, b]
  Matrix.identity_matrix(n)      -> Create an n x n identity matrix

Display:
  obj.show(name)                -> Print the matrix with a label
  str(obj)                      -> Print matrix directly (uses show)

Operations:
  m1 + m2                       -> Matrix addition
  m1 - m2                       -> Matrix subtraction
  m1 * m2                       -> Matrix multiplication
  num * m1                      -> Scalar multiplication
  m1 == m2                      -> Check equality
  m1 ^ m2                        -> Element-wise product (Hadamard)

Matrix Functions:
  obj.transpose(type)           -> Transpose matrix
                                   type='modify' changes current matrix
                                   type='new' returns a new transposed matrix
  obj.det()                     -> Determinant of square matrix
  obj.adjoint()                 -> Adjoint of square matrix
  obj.inverse()                 -> Inverse of square matrix
  obj.trace()                   -> Trace of square matrix
  obj.Frobenius_norm()          -> Frobenius norm (sqrt of sum of squares)
  obj.orthogonal_check()        -> Returns True if matrix is orthogonal

Other:
  obj.order()                   -> Returns string with matrix order (rows X columns)

Notes:
  - Use .show() to pretty print.
  - All operations are done in fully expanded element-wise loops.
  - Only square matrices can have determinant, inverse, trace, and adjoint.
===================================================
"""
        print(msg)