import React from 'react';


export default function PageHome() {
  return (
    <footer className="footer">
      <div className="footerLinks">
        <ul>
          <li>
            <span>INFORMATION</span>
            <ul>
              <li>
                <a href="/about/">About us</a>
              </li>
              <li>
                <a href="/create/">Create new page</a>
              </li>
              <li>
                <a href="/feedback/">Feedback</a>
              </li>
              <li>
                <a href="/webgl/">Unity</a>
              </li>
              <li>
                <a href="/donation/">Donation</a>
              </li>
            </ul>
          </li>
        </ul>
        <ul>
          <li>
            <span>ALTERNATIVE VIEW</span>
            <ul>
              <li>
                <a href="/graph/">Graph</a>
              </li>
              <li>
                <a href="/diagram/">Diagram</a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </footer>
  );
}
