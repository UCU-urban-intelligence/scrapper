import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import AppDrawer from './Drawer';

ReactDOM.render(
  <div className={{ display: 'flex' }}>
    <AppBar position="static" color="default">
      <Toolbar>
      </Toolbar>
    </AppBar>
    <AppDrawer></AppDrawer>
    <main className={{
      flexGrow: 1,
      padding: '18px',
      height: '100vh',
      overflow: 'auto',
    }}>
      <App></App>
    </main>
  </div>,
  document.getElementById('root')
);

// import initMap from './map'
// initMap(document.getElementById('root'))
