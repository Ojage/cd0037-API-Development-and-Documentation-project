import React, { Component } from 'react';
import styles from '../stylesheets/Header.module.css';

class Header extends Component {
  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <div className={`App-header ${styles.header}`}>
        <h1
          onClick={() => {
            this.navTo('');
          }}
        >
          Udacitrivia
        </h1>
        <h2
          onClick={() => {
            this.navTo('');
          }}
        >
          List
        </h2>
        <h2
          onClick={() => {
            this.navTo('/add');
          }}
        >
          Add
        </h2>
        <h2
          onClick={() => {
            this.navTo('/play');
          }}
        >
          Play
        </h2>
      </div>
    );
  }
}

export default Header;
