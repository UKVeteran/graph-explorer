import numpy as np
import sympy as sp

x_sym = sp.Symbol('x')

def analyze_function(fn_type, params, x_eval=0.0):
    """
    Analyzes the dynamic function: calculates values, roots, y-intercept, 
    turning points, and exact gradient at x_eval.
    """
    if fn_type == "Linear":
        m, c = params['m'], params['c']
        expr = m * x_sym + c
    elif fn_type == "Quadratic":
        a, b, c = params['a'], params['b'], params['c']
        expr = a * x_sym**2 + b * x_sym + c
    elif fn_type == "Exponential":
        a, b, c = params['a'], params['b'], params['c']
        expr = a * (b**x_sym) + c
    elif fn_type == "Trigonometric":
        a, b, c, d = params['a'], params['b'], params['c'], params['d']
        expr = a * sp.sin(b * x_sym + c) + d
    else:
        expr = x_sym

    # LaTeX string representation
    latex_repr = sp.latex(expr)

    # Numerical vector evaluation for Plotly
    f_num = sp.lambdify(x_sym, expr, 'numpy')
    x_vals = np.linspace(-10, 10, 500)
    try:
        y_vals = f_num(x_vals)
        if np.isscalar(y_vals):
            y_vals = np.full_like(x_vals, y_vals)
    except Exception:
        y_vals = np.zeros_like(x_vals)

    # Key Mathematical Properties
    # Y-intercept
    y_intercept = float(expr.subs(x_sym, 0).evalf())

    # Roots / X-intercepts
    try:
        roots_sol = sp.solve(expr, x_sym)
        real_roots = [float(r.evalf()) for r in roots_sol if r.is_real and -10 <= r <= 10]
    except Exception:
        real_roots = []

    # Derivative & Gradient
    deriv = sp.diff(expr, x_sym)
    gradient = float(deriv.subs(x_sym, x_eval).evalf())

    # Turning Points (Critical points)
    turning_points = []
    try:
        crit_pts = sp.solve(deriv, x_sym)
        for cp in crit_pts:
            if cp.is_real and -10 <= cp <= 10:
                cp_val = float(cp.evalf())
                y_cp = float(expr.subs(x_sym, cp).evalf())
                second_deriv = sp.diff(deriv, x_sym).subs(x_sym, cp).evalf()
                pt_type = "Minimum" if second_deriv > 0 else ("Maximum" if second_deriv < 0 else "Inflection")
                turning_points.append((cp_val, y_cp, pt_type))
    except Exception:
        pass

    return {
        "expr": expr,
        "latex": latex_repr,
        "x_vals": x_vals,
        "y_vals": y_vals,
        "y_intercept": y_intercept,
        "roots": real_roots,
        "gradient": gradient,
        "turning_points": turning_points
    }
