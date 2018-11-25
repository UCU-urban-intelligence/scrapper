import {Component} from "react";
import Divider from "@material-ui/core/Divider/Divider";
import List from "@material-ui/core/List/List";
import ListItem from "@material-ui/core/ListItem/ListItem";
import ListItemText from "@material-ui/core/ListItemText/ListItemText";
import Drawer from "@material-ui/core/Drawer/Drawer";
import React from "react";

class AppDrawer extends Component {
  render() {
    return (
      <Drawer variant="permanent" open={true}>
        <List>
          <ListItem button>
            <ListItemText primary="Dashboard" />
          </ListItem>
          <ListItem button>
            <ListItemText primary="Map" />
          </ListItem>
          <ListItem button>
            <ListItemText primary="Forecast" />
          </ListItem>
          <ListItem button>
            <ListItemText primary="Feedback" />
          </ListItem>
          <ListItem button>
            <ListItemText primary="Settings" />
          </ListItem>
        </List>
        <Divider />
      </Drawer>
    )
  }
}

export default AppDrawer;