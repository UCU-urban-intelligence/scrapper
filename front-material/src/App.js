import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import { mainListItems } from './listItems';
import { Switch, Route } from 'react-router-dom';
import Analytics from "./routes/Analytics";
import DarkMap from "./routes/DarkMap";
import Forecast from "./routes/Forecast";
import Settings from "./routes/Settings";
import Feedback from "./routes/Feedback";
import ListItem from "@material-ui/core/ListItem/ListItem";
import ListItemText from "@material-ui/core/ListItemText/ListItemText";
import ListItemIcon from "@material-ui/core/ListItemIcon/ListItemIcon";
import Map from "@material-ui/core/SvgIcon/SvgIcon";

const drawerWidth = 240;

const styles = theme => ({
  root: {
    display: 'flex',
  },
  toolbar: {
    paddingRight: 24, // keep right padding when drawer closed
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginLeft: 12,
    marginRight: 36,
  },
  menuButtonHidden: {
    display: 'none',
  },
  title: {
    flexGrow: 1,
  },
  drawerPaper: {
    position: 'relative',
    whiteSpace: 'nowrap',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  content: {
    flexGrow: 1,
    padding: 0,
    height: '100vh',
    overflow: 'auto',
  },
  h5: {
    marginBottom: theme.spacing.unit * 2,
  },
});

class App extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      geojson: {},
      popupData: undefined
    }
  };

  componentDidMount() {
    fetch('/out__Toronto.geojson')
    .then(response => {
      return response.json()
    })
    .then(geojson => {
      this.setState({
        geojson
      })
    })
  }

  addFeatureList(popupData) {
    this.setState({ popupData })
  }

  render() {
    const { classes } = this.props;
    const { popupData } = this.state;
    return (
      <div className={classes.root}>
        <CssBaseline />
        <AppBar
          position="absolute"
          className={classNames(classes.appBar, classes.appBarShift)}
        >
          <Toolbar className={classes.toolbar} style={{ backgroundColor: '#4d9221' }}>
            <IconButton
              color="inherit"
              className={classNames(
                classes.menuButton,
                classes.menuButtonHidden,
              )}
            >
              <MenuIcon />
            </IconButton>
            <Typography
              component="h1"
              variant="h6"
              color="inherit"
              noWrap
              className={classes.title}
            >
              Dashboard
            </Typography>
          </Toolbar>
        </AppBar>
        <Drawer
          variant="permanent"
          classes={{ paper: classNames(classes.drawerPaper) }}
          open={true}
        >
          <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <img src="./images/picture.png" alt="" style={{height: '90px'}}/>
          </div>
          <Divider />
          <List>{mainListItems}</List>
          <Divider />
          <List>
            <div>
              {!popupData || (() => {
                const data = ['efficiency'];
                for(let i in popupData) {
                  if(['coordinates', 'efficiency'].indexOf(i) !== -1) continue;
                  data.push(i);
                }
                console.log(data);
                return data.map((item, i) => {
                  console.log(item);
                  return (
                    <ListItem key={i} style={{padding: "0 24px" }}>
                      <ListItemIcon>
                        <Map />
                      </ListItemIcon>
                      <ListItemText style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: 0}}
                        primary={(item[0].toUpperCase() + item.substr(1)).split('_').join(' ') + ":"}
                        secondary={Math.round(popupData[item]*1000) / 1000} />
                    </ListItem>
                  )
                })
              })()}
            </div>
          </List>
        </Drawer>
        <main className={classes.content}>
          <Switch>
            <Route path='/' component={Analytics} exact/>
            <Route path='/map' render={(props) => <DarkMap
              {...props}
              geojson={this.state.geojson}
              updateFeatures={this.addFeatureList.bind(this)} />}
            />
            <Route path='/forecast' component={Forecast}/>
            <Route path='/feedback' component={Feedback}/>
            <Route path='/settings' component={Settings}/>
          </Switch>
        </main>
      </div>
    );
  }
}

App.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(App);
