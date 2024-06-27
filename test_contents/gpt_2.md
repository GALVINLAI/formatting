TEST 2


### Lemma 4.6 (Variance and Expectation)
Let \(X\) be a random variable in \(\mathbb{R}^d\).

1. For all \(y \in \mathbb{R}^d\), \(\mathbb{V}[X] \leq \mathbb{E}\left[\|X - y\|^2\right]\).

2. \(\mathbb{V}[X] \leq \mathbb{E}\left[\|X\|^2\right]\).

### Proof

**Item 2** is a direct consequence of Item 1 with \(y = 0\). We will focus on proving Item 1.

#### Proof of Item 1

To prove Item 1, we use the given identity and take the expectation.

1. **Identity Decomposition**:
   \[
   \|X - \mathbb{E}[X]\|^2 = \|X - y\|^2 + \|y - \mathbb{E}[X]\|^2 + 2 \langle X - y, y - \mathbb{E}[X] \rangle
   \]

   This identity can be derived from the fact that \((a - b)^2 = a^2 - 2ab + b^2\) in vector form. Let's break it down:

   - \( \|X - y\|^2 \): The squared distance between \(X\) and an arbitrary point \(y\).
   - \( \|y - \mathbb{E}[X]\|^2 \): The squared distance between the point \(y\) and the expectation \(\mathbb{E}[X]\).
   - \( 2 \langle X - y, y - \mathbb{E}[X] \rangle \): The cross term that represents the inner product.

2. **Taking Expectation**:
   Now, take the expectation of both sides of the identity:

   \[
   \mathbb{E}[\|X - \mathbb{E}[X]\|^2] = \mathbb{E}[\|X - y\|^2] + \mathbb{E}[\|y - \mathbb{E}[X]\|^2] + 2 \mathbb{E}[\langle X - y, y - \mathbb{E}[X] \rangle]
   \]

   We need to evaluate each term on the right-hand side.

   - \(\mathbb{E}[\|X - y\|^2]\): This term remains as it is.
   - \(\mathbb{E}[\|y - \mathbb{E}[X]\|^2]\): This term is constant with respect to \(X\) since \(y\) and \(\mathbb{E}[X]\) are fixed points.
   - \(2 \mathbb{E}[\langle X - y, y - \mathbb{E}[X] \rangle]\): This term simplifies because \(\mathbb{E}[X - y] = \mathbb{E}[X] - y\).

3. **Simplification of the Cross Term**:
   Let's simplify the cross term:

   \[
   \mathbb{E}[\langle X - y, y - \mathbb{E}[X] \rangle] = \langle \mathbb{E}[X - y], y - \mathbb{E}[X] \rangle = \langle \mathbb{E}[X] - y, y - \mathbb{E}[X] \rangle
   \]

   Since \(\langle \mathbb{E}[X] - y, y - \mathbb{E}[X] \rangle = - \|y - \mathbb{E}[X]\|^2\), we get:

   \[
   2 \mathbb{E}[\langle X - y, y - \mathbb{E}[X] \rangle] = 2(-\|y - \mathbb{E}[X]\|^2) = -2 \|y - \mathbb{E}[X]\|^2
   \]

4. **Combining Terms**:
   Substitute back into the expectation equation:

   \[
   \mathbb{E}[\|X - \mathbb{E}[X]\|^2] = \mathbb{E}[\|X - y\|^2] + \|y - \mathbb{E}[X]\|^2 - 2 \|y - \mathbb{E}[X]\|^2
   \]

   Simplify:

   \[
   \mathbb{E}[\|X - \mathbb{E}[X]\|^2] = \mathbb{E}[\|X - y\|^2] - \|y - \mathbb{E}[X]\|^2
   \]

   This simplifies further to:

   \[
   \mathbb{E}[\|X - \mathbb{E}[X]\|^2] = \mathbb{E}[\|X - y\|^2] - \|y - \mathbb{E}[X]\|^2 \leq \mathbb{E}[\|X - y\|^2]
   \]

   The inequality holds because \(\|y - \mathbb{E}[X]\|^2\) is a non-negative term.

Thus, we have shown that:

\[
\mathbb{V}[X] \leq \mathbb{E}[\|X - y\|^2]
\]

### Conclusion
The proof uses the identity for the squared distance between a random variable and its expectation, decomposes it into three terms, and then takes the expectation to show that the variance is always less than or equal to the expectation of the squared distance to any arbitrary point \(y\). This demonstrates the desired inequality and completes the proof.