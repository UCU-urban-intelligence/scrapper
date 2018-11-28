import React from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import DashboardIcon from '@material-ui/icons/Dashboard';
import ShoppingCartIcon from '@material-ui/icons/ShoppingCart';
import Map from '@material-ui/icons/Map';
import PeopleIcon from '@material-ui/icons/People';
import BarChartIcon from '@material-ui/icons/BarChart';
import LayersIcon from '@material-ui/icons/Layers';
import { NavLink } from 'react-router-dom';

export const mainListItems = (
  <div>
    <NavLink to='/'>
      <ListItem button>
        <ListItemIcon>
          <DashboardIcon />
        </ListItemIcon>
        <ListItemText primary="Analytics" />
      </ListItem>
    </NavLink>
    <NavLink to='/map'>
      <ListItem button>
        <ListItemIcon>
          <Map />
        </ListItemIcon>
        <ListItemText primary="Map" />
      </ListItem>
    </NavLink>
    <NavLink to='/forecast'>
      <ListItem button>
        <ListItemIcon>
          <BarChartIcon />
        </ListItemIcon>
        <ListItemText primary="Forecast" />
      </ListItem>
    </NavLink>
    <NavLink to='/feedback'>
      <ListItem button>
        <ListItemIcon>
          <PeopleIcon />
        </ListItemIcon>
        <ListItemText primary="Feedback" />
      </ListItem>
    </NavLink>
    <NavLink to='/settings'>
      <ListItem button>
        <ListItemIcon>
          <LayersIcon />
        </ListItemIcon>
        <ListItemText primary="Settings" />
      </ListItem>
    </NavLink>
  </div>
);
