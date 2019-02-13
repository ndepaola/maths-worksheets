from pylatex import Section, NoEscape
import random
from sympy import *


def _rexppoly(n, o):
    """
    Function generation helper function
    Return a list of e^f(x), where f(x) is an o-order polynomial, as Sympy objects
    """
    fcns = []
    poly_fcns = _rpoly(n, o)
    for eq in poly_fcns:
        x, y = symbols("x y")
        fcns.append(Eq(y, exp(eq.rhs)))
    return fcns


def _rparam(a, b, p):
    """
    Parameter generation helper function
    Return a random number between a and b, with p decimal places of precision
    """
    return round(a + (b-a)*random.random(), p)


def _rpoly(n, o):
    """
    Function generation helper function
    Return a list of n o-order polynomials as Sympy objects
    """
    fcns = []
    for _ in range(0, n):
        x, y, z = symbols("x y z")
        z = 0
        # Generate o coefficients
        for i in range(0, o):
            z += int(_rparam(0, 8, 0))*pow(x, i)
        y = Eq(y, z)
        fcns.append(y)
    return fcns


def _rtrig(n):
    """
    Function generation helper function
    Return a list of n trig functions as Sympy objects
    """
    fcns = []
    for _ in range(0, n):
        x, y = symbols("x y")
        a = int(_rparam(1, 15, 0))
        b = random.choice([Rational(1, 4),
                           Rational(1, 2),
                           Rational(3, 4),
                           Rational(3, 2), 1])

        c = random.choice([Rational(1, 8),
                           Rational(3, 16),
                           Rational(5, 12),
                           Rational(8, 9), 4])

        y = Eq(y, a*sin(b*pi*x + c*pi))
        fcns.append(y)
    return fcns


class ChainRule:
    """
    Include chain rule problems in the sheet. These questions only
    require one application of the chain rule to solve. This can
    be inherited and passed different types of functions for u,
    but it defaults to polynomials.
    """

    u_subs = []
    fcns = []
    n_cols = 3

    @staticmethod
    def leading_text():
        # Text to attach to the front of the question. "Solve this"
        return "Find the derivatives of the following functions using u-substitution (chain rule):"

    @staticmethod
    def default_num():
        # Default number of this question to include in a worksheet.
        return 6

    def __str__(self):
        # Name of the topic, suitable to print to topic blurb
        return "Chain rule"

    def __init__(self, n=0, eq=None, append=False):
        # Create randomly generated parameters and store them as class variables
        # Parameters should be n-element lists, where n is the number of questions
        # you want to generate of this type.
        # We can also expand the inputs here to include a difficulty setting, and that
        # could affect how parameters are generated.
        # I've included a helper function <rparam> here to make it simpler to generate
        # parameters between a certain range and with a specified decimal precision.
        if eq is not None:
            u_subs = eq
        else:
            # Default to polynomials
            u_subs = _rpoly(o=3, n=n)  # 3rd order to make things less horrible (x^2)

        fcns = []
        self.u_subs = u_subs
        for eq in u_subs:
            x, y = symbols("x y")
            selector = random.random()
            if selector < 0.2:
                # Polynomials in brackets to a power
                power =_rparam(2, 9, 0)
                fcns.append(Eq(y, pow(eq.rhs, int(power))))

            elif selector < 0.4:
                # Polynomials in square root
                fcns.append(Eq(y, sqrt(eq.rhs)))

            elif selector < 0.6:
                # 1 / polynomial
                numerator = _rparam(2, 9, 0)
                fcns.append(Eq(y, int(numerator) / eq.rhs))

            elif selector < 0.8:
                # e to the power of polynomial
                fcns.append(Eq(y, exp(eq.rhs)))

            else:
                # log of polynomial
                fcns.append(Eq(y, log(eq.rhs)))

        # Insert the selected equations
        if append and self.fcns is not None:
            self.fcns += fcns
        else:
            self.fcns = fcns

    def insert_question(self, doc):
        with doc.create(Section(str(self))):
            # Generate the LaTeX code to insert each question of this topic into the document.
            doc.append(self.leading_text())
            doc.append(NoEscape(r'\begin{multicols}{%i}' % self.n_cols))
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.fcns)):
                doc.append(NoEscape(r'\item \[%s \]' % latex(self.fcns[i])))
            doc.append(NoEscape(r'\end{enumerate}'))
            doc.append(NoEscape(r'\end{multicols}'))
            return doc

    def insert_answer(self, doc):
        with doc.create(Section(str(self))):
            x, u = symbols("x u")
            # Generate the LaTeX code to insert each worked answer of this topic into the
            # document.
            # doc.append(NoEscape(r'\begin{multicols}{2}'))  # Can split up solution across columns
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.fcns)):
                # dy/dx = d/dx(f(x)) = the derivative, spat out by sympy
                doc.append(NoEscape(r'\item \[ \frac{dy}{dx} = \frac{d}{dx} \left[ %s \right] \]'
                                    % latex(self.fcns[i].rhs)))

                doc.append(NoEscape("Solve with $u$-substitution:"))
                doc.append(NoEscape(r'\[ \frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx},\: u = %s \]'
                                    % latex(self.u_subs[i].rhs)))
                doc.append(NoEscape(r'Calculate $\displaystyle \frac{dy}{du}$ '
                                    r'and $\displaystyle \frac{du}{dx}$:'))
                doc.append(NoEscape(r'\[ y(u) = %s \text{, so } \frac{dy}{du} = %s \]'
                                    % (latex(self.fcns[i].rhs.subs(self.u_subs[i].rhs, u)),
                                       latex(diff(self.fcns[i].rhs.subs(self.u_subs[i].rhs, u))))))
                doc.append(NoEscape(r'\[ \frac{du}{dx} = \frac{d}{dx}\left[ %s \right] = %s \]'
                                    % (latex(self.u_subs[i].rhs),
                                       latex(diff(self.u_subs[i].rhs)))))
                doc.append(NoEscape("Substitute into chain rule equation:"))
                doc.append(NoEscape(r'\[ \frac{dy}{dx} = \left[ %s \right] \cdot \left[ %s \right] \]'
                                    % (latex(diff(self.fcns[i].rhs.subs(self.u_subs[i].rhs, u))),
                                       latex(diff(self.u_subs[i].rhs)))))
                doc.append(NoEscape(r'\[ \frac{dy}{dx} = %s \]' % latex(diff(self.fcns[i].rhs))))
            doc.append(NoEscape(r'\end{enumerate}'))
            # doc.append(NoEscape(r'\end{multicols}'))
            return doc


# TODO: Finish implementing this class
class ProductRule:
    """
    Include chain rule problems in the sheet. These questions only
    require one application of the chain rule to solve. This can
    be inherited and passed different types of functions for u,
    but it defaults to polynomials.
    """

    fcn_u = []
    fcn_v = []
    fcns = []
    n_cols = 3

    @staticmethod
    def leading_text():
        # Text to attach to the front of the question. "Solve this"
        return "Find the derivatives of the following functions using the product rule:"

    @staticmethod
    def default_num():
        # Default number of this question to include in a worksheet.
        return 6

    def __str__(self):
        # Name of the topic, suitable to print to topic blurb
        return "Product rule"

    def __init__(self, n=0, eq=None, append=False):
        # Create randomly generated parameters and store them as class variables
        # Parameters should be n-element lists, where n is the number of questions
        # you want to generate of this type.
        # We can also expand the inputs here to include a difficulty setting, and that
        # could affect how parameters are generated.
        # I've included a helper function <rparam> here to make it simpler to generate
        # parameters between a certain range and with a specified decimal precision.
        if eq is not None:
            u_subs = eq
        else:
            # Default to polynomials
            u_subs = _rpoly(o=3, n=n)  # 3rd order to make things less horrible (x^2)

        fcns = []
        self.u_subs = u_subs
        for eq in u_subs:
            x, y = symbols("x y")
            selector = random.random()
            if selector < 0.2:
                # Polynomials in brackets to a power
                power =_rparam(2, 9, 0)
                fcns.append(Eq(y, pow(eq.rhs, int(power))))

            elif selector < 0.4:
                # Polynomials in square root
                fcns.append(Eq(y, sqrt(eq.rhs)))

            elif selector < 0.6:
                # 1 / polynomial
                numerator = _rparam(2, 9, 0)
                fcns.append(Eq(y, int(numerator) / eq.rhs))

            elif selector < 0.8:
                # e to the power of polynomial
                fcns.append(Eq(y, exp(eq.rhs)))

            else:
                # log of polynomial
                fcns.append(Eq(y, log(eq.rhs)))

        # Insert the selected equations
        if append and self.fcns is not None:
            self.fcns += fcns
        else:
            self.fcns = fcns

    def insert_question(self, doc):
        with doc.create(Section(str(self))):
            # Generate the LaTeX code to insert each question of this topic into the document.
            doc.append(self.leading_text())
            doc.append(NoEscape(r'\begin{multicols}{%i}' % self.n_cols))
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.fcns)):
                doc.append(NoEscape(r'\item \[%s \]' % latex(self.fcns[i])))
            doc.append(NoEscape(r'\end{enumerate}'))
            doc.append(NoEscape(r'\end{multicols}'))
            return doc

    def insert_answer(self, doc):
        with doc.create(Section(str(self))):
            x, u = symbols("x u")
            # Generate the LaTeX code to insert each worked answer of this topic into the
            # document.
            # doc.append(NoEscape(r'\begin{multicols}{2}'))  # Can split up solution across columns
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.fcns)):
                # dy/dx = d/dx(f(x)) = the derivative, spat out by sympy
                doc.append(NoEscape(r'\item \[ \frac{dy}{dx} = \frac{d}{dx} \left[ %s \right] \]'
                                    % latex(self.fcns[i].rhs)))

                doc.append(NoEscape("Solve with product rule:"))
                doc.append(NoEscape(r'\[ \frac{dy}{dx} = u\' \cdot v ,\: y = u \cdot v \]'))
                doc.append(NoEscape(r'Calculate $\displaystyle \frac{dy}{du}$ '
                                    r'and $\displaystyle \frac{du}{dx}$:'))
                doc.append(NoEscape(r'\[ y(u) = %s \text{, so } \frac{dy}{du} = %s \]'
                                    % (latex(self.fcns[i].rhs.subs(self.u_subs[i].rhs, u)),
                                       latex(diff(self.fcns[i].rhs.subs(self.u_subs[i].rhs, u))))))
                doc.append(NoEscape(r'\[ \frac{du}{dx} = \frac{d}{dx}\left[ %s \right] = %s \]'
                                    % (latex(self.u_subs[i].rhs),
                                       latex(diff(self.u_subs[i].rhs)))))
                doc.append(NoEscape("Substitute into chain rule equation:"))
                doc.append(NoEscape(r'\[ \frac{dy}{dx} = \left[ %s \right] \cdot \left[ %s \right] \]'
                                    % (latex(diff(self.fcns[i].rhs.subs(self.u_subs[i].rhs, u))),
                                       latex(diff(self.u_subs[i].rhs)))))
                doc.append(NoEscape(r'\[ \frac{dy}{dx} = %s \]' % latex(diff(self.fcns[i].rhs))))
            doc.append(NoEscape(r'\end{enumerate}'))
            # doc.append(NoEscape(r'\end{multicols}'))
            return doc


class SimpleDerivative:

    """
    Include simple derivative questions in the sheet. One line
    of working for the solution. This can be inherited and passed
    different types of functions, but it defaults to polynomials.
    """

    fcns = []
    n_cols = 3

    @staticmethod
    def leading_text():
        # Text to attach to the front of the question. "Solve this"
        return "Find the derivatives of the following functions:"

    @staticmethod
    def default_num():
        # Default number of this question to include in a worksheet.
        return 6

    def __str__(self):
        # Name of the topic, suitable to print to topic blurb
        return "Simple derivatives"

    def __init__(self, n=0, eq=None, append=False):
        # Create randomly generated parameters and store them as class variables
        # Parameters should be n-element lists, where n is the number of questions
        # you want to generate of this type.
        # We can also expand the inputs here to include a difficulty setting, and that
        # could affect how parameters are generated.
        # I've included a helper function <rparam> here to make it simpler to generate
        # parameters between a certain range and with a specified decimal precision.
        if eq is not None:
            fcns = eq
        else:
            # Default to polynomials
            fcns = _rpoly(o=4, n=n)

        # Insert the selected equations
        if append and self.fcns is not None:
            self.fcns += fcns
        else:
            self.fcns = fcns

    def insert_question(self, doc):
        with doc.create(Section(str(self))):
            # Generate the LaTeX code to insert each question of this topic into the document.
            doc.append(self.leading_text())
            doc.append(NoEscape(r'\begin{multicols}{%i}' % self.n_cols))
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.fcns)):
                doc.append(NoEscape(r'\item \[%s \]' % latex(self.fcns[i])))
            doc.append(NoEscape(r'\end{enumerate}'))
            doc.append(NoEscape(r'\end{multicols}'))
            return doc

    def insert_answer(self, doc):
        with doc.create(Section(str(self))):
            x = symbols("x")
            # Generate the LaTeX code to insert each worked answer of this topic into the
            # document.
            doc.append(NoEscape(r'\begin{multicols}{2}'))
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.fcns)):
                doc.append(NoEscape(r'\item \begin{align*}'))
                # dy/dx = d/dx(f(x)) = the derivative, spat out by sympy
                doc.append(NoEscape(r'\frac{dy}{dx} &= \frac{d}{dx} \left[ %s \right] \\'
                                    % latex(self.fcns[i].rhs)))
                doc.append(NoEscape(r'&= %s' % latex(diff(self.fcns[i].rhs))))
                doc.append(NoEscape(r'\end{align*}'))
            doc.append(NoEscape(r'\end{enumerate}'))
            doc.append(NoEscape(r'\end{multicols}'))
            return doc


class SimpleDerivatives(SimpleDerivative):

    """
    Include a selection of 8 simple derivative questions,
    with a mix of polynomials and trig functions.
    """

    @staticmethod
    def default_num():
        # Default number of this question to include in a worksheet.
        return 8  # Multiples of 4 please

    def __init__(self, n):
        # Eight questions, mixed between polynomials and trig, then shuffled
        a = random.randint(2, n-2)
        b = n-a
        print(a+b)
        self.n_cols = 4
        SimpleDerivative.__init__(self, n=a, append=False)
        SimpleDerivative.__init__(self, eq=_rtrig(b), append=True)
        random.shuffle(self.fcns)


class FirstPrinciples:
    fcns = []

    @staticmethod
    def leading_text():
        # Text to attach to the front of the question. "Solve this"
        return "Find the derivatives of the following functions using first principles:"

    @staticmethod
    def default_num():
        # Default number of this question to include in a worksheet.
        return 4

    def __str__(self):
        # Name of the topic, suitable to print to topic blurb
        return "First principles"

    def __init__(self, n):
        # Create randomly generated parameters and store them as class variables
        # Parameters should be n-element lists, where n is the number of questions
        # you want to generate of this type.
        # We can also expand the inputs here to include a difficulty setting, and that
        # could affect how parameters are generated.
        # I've included a helper function <rparam> here to make it simpler to generate
        # parameters between a certain range and with a specified decimal precision.
        # Default to polynomials
        fcns = _rpoly(o=4, n=n)
        self.fcns = fcns

    def insert_question(self, doc):
        with doc.create(Section(str(self))):

            # Generate the LaTeX code to insert each question of this topic into the document.
            doc.append(self.leading_text())
            doc.append(NoEscape(r'\begin{multicols}{4}'))
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.fcns)):
                doc.append(NoEscape(r'\item \[%s \]' % latex(self.fcns[i])))
            doc.append(NoEscape(r'\end{enumerate}'))
            doc.append(NoEscape(r'\end{multicols}'))
            return doc

    def insert_answer(self, doc):
        with doc.create(Section(str(self))):
            x, h = symbols("x h")
            # Generate the LaTeX code to insert each worked answer of this topic into the
            # document.
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.fcns)):
                doc.append(NoEscape(r'\item \begin{align*}'))
                doc.append(NoEscape(r'\frac{dy}{dx} &= \lim_{h \rightarrow 0} \left['
                                    r'\frac{f(x+h) - f(x)}{h} \right],\: f(x) = %s \\'
                                    % latex(self.fcns[i].rhs)))
                doc.append(NoEscape(r'&= \lim_{h \rightarrow 0} \left[ \frac{[%s] - [%s]}{h} \right] \\'
                                    % (latex(self.fcns[i].rhs.subs(x, x+h, )),
                                       latex(self.fcns[i].rhs))))
                expr = (self.fcns[i].rhs.subs(x, x+h, evaluate=False) -
                        self.fcns[i].rhs)/h
                doc.append(NoEscape(r'&= \lim_{h \rightarrow 0} \left[ %s \right] \\'
                                    % latex(expand(expr))))
                doc.append(NoEscape(r'&= %s' % latex(limit(expr, h, 0))))

                doc.append(NoEscape(r'\end{align*}'))
            doc.append(NoEscape(r'\end{enumerate}'))
            return doc
