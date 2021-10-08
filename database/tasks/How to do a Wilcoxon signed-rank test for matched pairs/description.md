
Assume we have two samples of data that come in matched pairs,
$x_1, x_2, x_3, \ldots x_k$ and $x'_1, x'_2, x'_3, \ldots x'_k$,
which we might pair up as $(x_1,x'_1),(x_2,x'_2),\ldots,(x_k,x'_k)$.
The two samples may be from different populations.
Also assume that the sample sizes are small or the populations are not normally
distributed.

Consider measuring the difference in each pair, $x_1-x'_1,x_2-x'_2,\ldots,x_k-x'_k$.
We want to perform tests that compare the median of those differences, $m_D$, to a
hypothesized value (equal, greater, or less). One method is the Wilcoxon
Signed-Rank Test for Matched Pairs.

Related tasks:

 * How to do a Kruskal-Wallis test
 * How to do a Wilcoxon rank-sum test
 * How to do a Wilcoxon signed-rank test
