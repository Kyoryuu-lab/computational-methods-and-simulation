<h1>computational-methods-and-simulation</h1>
<p>Numerical mathematics and scientific computing suite in Python: polynomial interpolation, epidemiological ODE modeling, and spatial Monte Carlo integration</p>

<h2>Project description</h2>
<p>This repository provides a modular, production-grade computational mathematics suite implementing foundational algorithms across numerical analysis, dynamic systems, and stochastic simulation:</p>
<ol>
  <li>
    <dl>
      <dt><b>Numerical Polynomial Interpolation:</b></dt>
      <dd>Implements Newton's divided difference algorithm to construct polynomial interpolants of degree $n$ without requiring matrix inversions.</dd>
      <dd>Evaluates polynomial representations efficiently using nested Horner schemes and compares results against piecewise linear interpolation.</dd>
    </dl>
  </li>
  <li>
    <dl>
      <dt><b>Epidemiological System Dynamics (SIR Model):</b></dt>
      <dd>Models transmission dynamics governed by nonlinear ordinary differential equations (ODE): $\frac{dS}{dt}$, $\frac{dI}{dt}$, $\frac{dR}{dt}$.</dd>
      <dd>Integrates time-dependent intervention steps simulating variable lockdown dates and contact reduction parameters ($\beta(t)$) via <code>scipy.integrate.odeint</code>.</dd>
      <dd>Calculates projected daily mortality curves and epidemic peak shifts.</dd>
    </dl>
  </li>
  <li>
    <dl>
      <dt><b>Spatial Monte Carlo Area Integration:</b></dt>
      <dd>Processes binary bitmap boundaries and extracts closed vector contours using OpenCV.</dd>
      <dd>Conducts uniform spatial random sampling ($N = 40,000$ points) inside the bounding box and evaluates topological inclusion via Shapely point-in-polygon tests.</dd>
      <dd>Calculates numerical surface approximations and estimates relative error margins against geographic ground-truth data.</dd>
    </dl>
  </li>
</ol>

<h2>Project files</h2>
<table>
  <tr>
    <th colspan="2">computational-methods-and-simulation</th>
  </tr>
  <tr>
    <td>main.py</td>
    <td>Master CLI orchestrator running the full numerical pipeline or individual modules</td>
  </tr>
  <tr>
    <td>modules/interpolation.py</td>
    <td>Newton divided difference scheme, Horner evaluation, and linear interpolation</td>
  </tr>
  <tr>
    <td>modules/epidemic_sir.py</td>
    <td>SIR differential equation solver and multi-scenario lockdown analysis</td>
  </tr>
  <tr>
    <td>modules/monte_carlo_area.py</td>
    <td>OpenCV boundary segmentation and Shapely-based Monte Carlo area integration</td>
  </tr>
  <tr>
    <td>README.md</td>
    <td>Mathematical documentation and operational guide</td>
  </tr>
  <tr>
    <td>.gitignore</td>
    <td>Exclusion rules for Python bytecode, virtual environments, and generated plots</td>
  </tr>
</table>

<h2>Mathematical Formulation</h2>
<table>
  <tr>
    <th>Domain</th>
    <th>Method</th>
    <th>Mathematical Model</th>
  </tr>
  <tr>
    <td><b>Interpolation</b></td>
    <td>Newton's Divided Differences</td>
    <td>$P_n(x) = f[x_0] + \sum_{k=1}^n f[x_0, \dots, x_k] \prod_{j=0}^{k-1} (x - x_j)$</td>
  </tr>
  <tr>
    <td><b>Dynamic Systems</b></td>
    <td>SIR Differential Equations</td>
    <td>$\frac{dS}{dt} = -\frac{\beta(t) S I}{N}, \quad \frac{dI}{dt} = \frac{\beta(t) S I}{N} - \gamma I, \quad \frac{dR}{dt} = \gamma I$</td>
  </tr>
  <tr>
    <td><b>Stochastic Simulation</b></td>
    <td>Monte Carlo Integration</td>
    <td>$A_{\text{est}} \approx A_{\text{box}} \cdot \frac{N_{\text{inside}}}{N_{\text{total}}}, \quad \epsilon = \frac{|A_{\text{est}} - A_{\text{real}}|}{A_{\text{real}}} \cdot 100\%$</td>
  </tr>
</table>

<h2>Installation and launch</h2>
<ol>
  <b>
    <li>
      <dl>
        <dt>Clone repository</dt>
        <dd>
          <code>git clone https://github.com/Kyoryuu-lab/computational-methods-and-simulation.git</code>
        </dd>
        <dd>
          <code>cd computational-methods-and-simulation</code>
        </dd>
      </dl>
    </li>
  </b>
  <b>
    <li>
      <dl>
        <dt>Install dependencies</dt>
        <dd>
          <code>pip install numpy scipy matplotlib opencv-python shapely</code>
        </dd>
      </dl>
    </li>
  </b>
  <b>
    <li>
      <dl>
        <dt>Run complete numerical suite</dt>
        <dd>
          <code>python main.py --module all --save-plots</code>
        </dd>
        <dd>Execute individual modules: <code>python main.py --module epidemic</code> (Options: <code>interpolation</code>, <code>epidemic</code>, <code>montecarlo</code>)</dd>
      </dl>
    </li>
  </b>
</ol>

<h2>Example of console output (python main.py --module all)</h2>
<samp>
  <p>
    ==============================================================================<br />
    &nbsp;&nbsp;1. MODUL: NUMERISCHE POLYNOMINTERPOLATION<br />
    ==============================================================================<br />
    [*] Stützstellen x: [0.101, 0.106, 0.111, 0.116, 0.121, 0.126, 0.131, 0.136, 0.141, 0.146, 0.151]<br />
    [*] Evaluierungspunkte X: [0.1035, 0.1492, 0.1324, 0.159]<br />
    &nbsp;&nbsp;&nbsp;&nbsp;x = 0.1035 | Linear: 1.269135 | Newton: 1.269136<br />
    &nbsp;&nbsp;&nbsp;&nbsp;x = 0.1492 | Linear: 1.409958 | Newton: 1.409958<br />
    &nbsp;&nbsp;&nbsp;&nbsp;x = 0.1324 | Linear: 1.356455 | Newton: 1.356454<br />
    &nbsp;&nbsp;&nbsp;&nbsp;x = 0.1590 | Linear: 1.415790 | Newton: 1.442220<br />
    <br />
    ==============================================================================<br />
    &nbsp;&nbsp;2. MODUL: SIR-EPIDEMIEDYNAMIK (ODE-INTEGRATION)<br />
    ==============================================================================<br />
    [*] Starte SIR-Differentialgleichungsintegration...<br />
    &nbsp;&nbsp;&nbsp;&nbsp;- Szenario (Tag 30, -50%): Peak an Tag 71 | Max. tägliche Mortalität: 2.14e-04<br />
    &nbsp;&nbsp;&nbsp;&nbsp;- Szenario (Tag 50, -70%): Peak an Tag 50 | Max. tägliche Mortalität: 4.86e-04<br />
    &nbsp;&nbsp;&nbsp;&nbsp;- Szenario (Tag 70, -90%): Peak an Tag 70 | Max. tägliche Mortalität: 1.83e-03<br />
    <br />
    ==============================================================================<br />
    &nbsp;&nbsp;3. MODUL: MONTE-CARLO-FLÄCHENINTEGRATION<br />
    ==============================================================================<br />
    [*] Monte-Carlo-Integration (40,000 Punkte):<br />
    &nbsp;&nbsp;&nbsp;&nbsp;Punkte innerhalb : 26,482 / 40,000<br />
    &nbsp;&nbsp;&nbsp;&nbsp;Geschätzte Fläche: 6842.1500 km² (Referenz: 6890.0 km²)<br />
    &nbsp;&nbsp;&nbsp;&nbsp;Abweichung&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: 0.694 %<br />
    <br />
    ==============================================================================<br />
    &nbsp;&nbsp;ALLE NUMERISCHEN BERECHNUNGEN ERFOLGREICH ABGESCHLOSSEN.<br />
    ==============================================================================
  </p>
