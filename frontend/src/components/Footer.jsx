import React from 'react';
import './Footer.css';

export default function PageHome() {
  return (
    <footer className="footer">
      <div className="footerLinks">
        <ul>
          <li>
            <span>INFORMATION</span>
            <ul>
              <li>
                <a href="/backend/about/">About us</a>
              </li>
              <li>
                <a href="/backend/create/">Create new page</a>
              </li>
              <li>
                <a href="/backend/feedback/">Feedback</a>
              </li>
              <li>
                <a href="/webgl/">Unity</a>
              </li>
              <li>
                <a href="/backend/donation/">Donation</a>
              </li>
            </ul>
          </li>
        </ul>
        <ul>
          <li>
            <span>ALTERNATIVE VIEW</span>
            <ul>
              <li>
                <a href="/backend/graph/">Graph</a>
              </li>
              <li>
                <a href="/backend/diagram/">Diagram</a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </footer>
  );
}
