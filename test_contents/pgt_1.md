TEST 1

### Example 1: Stochastic Gradient Descent (SGD) for Linear Regression

**Finite Sum Setting**:
- **Data**: \((\phi_i, y_i)\) for \(i = 1, \ldots, n\), where \(\phi_i \in \mathbb{R}^d\) and \(y_i \in \mathbb{R}\).
- **Objective**: Least-squares function 
  \[
  f(x) = \frac{1}{2n} \sum_{i=1}^n (\langle \phi_i, x \rangle - y_i)^2
  \]

**Expectation Setting**:
- **Data**: \((\phi, y)\) drawn from a distribution \(\mathcal{D}\).
- **Objective**: Expected least-squares function
  \[
  f(x) = \mathbb{E}_{(\phi, y) \sim \mathcal{D}} \left[ \frac{1}{2} (\langle \phi, x \rangle - y)^2 \right]
  \]


### Example 2: Logistic Regression

**Finite Sum Setting**:
- **Data**: \((\phi_i, y_i)\) for \(i = 1, \ldots, n\), where \(\phi_i \in \mathbb{R}^d\) and \(y_i \in \{0, 1\}\).
- **Objective**: Sum of logistic loss functions
  \[
  f(x) = \frac{1}{n} \sum_{i=1}^n \left( \log(1 + \exp(-y_i \langle \phi_i, x \rangle)) \right)
  \]

**Expectation Setting**:
- **Data**: \((\phi, y)\) drawn from a distribution \(\mathcal{D}\).
- **Objective**: Expected logistic loss function
  \[
  f(x) = \mathbb{E}_{(\phi, y) \sim \mathcal{D}} \left[ \log(1 + \exp(-y \langle \phi, x \rangle)) \right]
  \]

### Example 3: Regularized Risk Minimization

**Finite Sum Setting**:
- **Data**: \((\phi_i, y_i)\) for \(i = 1, \ldots, n\), where \(\phi_i \in \mathbb{R}^d\) and \(y_i \in \mathbb{R}\).
- **Objective**: Regularized least-squares function 
  \[
  f(x) = \frac{1}{2n} \sum_{i=1}^n (\langle \phi_i, x \rangle - y_i)^2 + \frac{\lambda}{2} \|x\|^2
  \]

**Expectation Setting**:
- **Data**: \((\phi, y)\) drawn from a distribution \(\mathcal{D}\).
- **Objective**: Expected regularized least-squares function
  \[
  f(x) = \mathbb{E}_{(\phi, y) \sim \mathcal{D}} \left[ \frac{1}{2} (\langle \phi, x \rangle - y)^2 \right] + \frac{\lambda}{2} \|x\|^2
  \]

### Example 4: Empirical Risk Minimization (ERM) in Machine Learning

**Finite Sum Setting**:
- **Data**: Training samples \(\{(\phi_i, y_i)\}_{i=1}^n\).
- **Objective**: Empirical risk (average loss over training set)
  \[
  f(x) = \frac{1}{n} \sum_{i=1}^n \ell(\phi_i, y_i; x)
  \]
  where \(\ell(\phi, y; x)\) is the loss function for sample \((\phi, y)\).

**Expectation Setting**:
- **Data**: Sample \((\phi, y)\) drawn from a distribution \(\mathcal{D}\).
- **Objective**: Expected risk (expected loss over the distribution)
  \[
  f(x) = \mathbb{E}_{(\phi, y) \sim \mathcal{D}} [ \ell(\phi, y; x) ]
  \]

### Summary
In these examples, the finite sum setting deals with a fixed dataset where the objective function is the sum or average of individual losses or errors. The expectation setting generalizes this to a stochastic framework where the objective function is the expected loss or error over a probability distribution. This shift from a finite sum to an expectation allows the application of stochastic optimization methods, such as Stochastic Gradient Descent (SGD), and extends the applicability of the results to scenarios where data is continuously drawn from a distribution rather than being fixed.