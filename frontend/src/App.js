import * as React from 'react';
import './App.css';
import SkipPreviousRoundedIcon from '@mui/icons-material/SkipPreviousRounded';
import SkipNextRoundedIcon from '@mui/icons-material/SkipNextRounded';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import LinearProgress from '@mui/material/LinearProgress';
import PauseRoundedIcon from '@mui/icons-material/PauseRounded';
import AddRoundedIcon from '@mui/icons-material/AddRounded';
import ListSubheader from '@mui/material/ListSubheader';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItem from '@mui/material/ListItem';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import DeleteIcon from '@mui/icons-material/Delete';
import PlayArrowRoundedIcon from '@mui/icons-material/PlayArrowRounded';
import ControlPointIcon from '@mui/icons-material/ControlPoint';
import IconButton from '@mui/material/IconButton';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import { Box } from '@mui/system';
import { Container } from '@mui/material';

function AddCompositionButton(props){
  return (
    <IconButton onClick={() => {props.onClick(props.index)}}>
      <AddRoundedIcon/>
    </IconButton>
  )
}

function DeletePlaylist(props){
  return (
    <IconButton onClick={() => {props.onClick(props.index)}}>
      <DeleteIcon/>
    </IconButton>
  )
}

function PlayComposition(props){
  return (
    <IconButton onClick={() => {props.onClick(props.index, props.compIndex)}}>
      <PlayArrowRoundedIcon/>
    </IconButton>
  )
}

function PushBack(props){
  return (
    <IconButton onClick={() => {props.onClick(props.index, props.compIndex)}}>
      <ExpandMore/>
    </IconButton>
  )
}

function PushForward(props){
  return (
    <IconButton onClick={() => {props.onClick(props.index, props.compIndex)}}>
      <ExpandLess/>
    </IconButton>
  )
}

function RemoveComposition(props){
  return (
    <IconButton onClick={() => {props.onClick(props.index, props.compIndex)}}>
      <DeleteIcon/>
    </IconButton>
  )
}

function AddMusicListButton(props){
  return (
    <ListItem>
      <ListItemButton onClick={() => {
          props.dialogCallback(props.index);
        }}>
        {props.name}
      </ListItemButton>
    </ListItem>
  )
}

class PlayListList extends React.Component{
  constructor(props){
    super(props);
    this.worksWith = -1;
    this.state = {playlists: [], currentPlaylist: -1, dialogOpened: false, music: []};
    this.addComposition = this.addComposition.bind(this);
    this.deletePlaylist = this.deletePlaylist.bind(this);
    this.playComposition = this.playComposition.bind(this);
    this.pushBack = this.pushBack.bind(this);
    this.pushForward = this.pushForward.bind(this);
    this.removeComposition = this.removeComposition.bind(this);
    this.openDialog = this.openDialog.bind(this);
    this.dialogCallback = this.dialogCallback.bind(this);
  }

  setData(data){
    this.setState({...this.state, playlists: data.playlists, currentPlaylist: data.current_playlist});
  }
  
  updateSelf(){
    fetch('/get_playlists', {
      method: 'POST',
      cache: 'no-cache'
    }).then((response) => response.json()).then((data) => {
      this.setData({...this.state, ...data});
    });
  }

  componentDidMount(){
    this.updateSelf();
    fetch('/get_music', {
      method: 'POST',
      cache: 'no-cache'
    }).then((response) => response.json()).then((data) => {
      this.setState({...this.state, music: data.music});
    });
  }

  dialogCallback(index){
    fetch('/add_composition', {
      method: 'POST',
      cache: 'no-cache',
      body: JSON.stringify({playlist_index: this.worksWith, music_index: index})
    }).then((response) => response.json()).then((data) => {
      this.setState({playlists: data.playlists, currentPlaylist: data.current_playlist, dialogOpened: false, music: this.state.music});
    });
  }

  addComposition(index){
    this.worksWith = index;
    this.setState({
      ...this.state,
      dialogOpened: true
    });
  }

  deletePlaylist(index){
    fetch('/remove_playlist', {
      method: 'POST',
      cache: 'no-cache',
      body: JSON.stringify({index: index})
    }).then((response) => response.json()).then((data) => {
      this.setData(data);
      this.props.updater();
    });
  }

  playComposition(index, compIndex){
    fetch('/play', {
      method: 'POST', 
      cache: 'no-cache',
      body: JSON.stringify({playlist_index: index, music_index: compIndex})
    }).then((response) => response.json()).then((data) => {
      this.setData(data);
      this.props.updater();
    });
  }

  pushBack(index, compIndex){
    fetch('/push_back', {
      method: 'POST', 
      cache: 'no-cache',
      body: JSON.stringify({playlist_index: index, music_index: compIndex})
    }).then((response) => response.json()).then((data) => {
      this.setData(data);
    });
  }

  pushForward(index, compIndex){
    fetch('/push_forward', {
      method: 'POST', 
      cache: 'no-cache',
      body: JSON.stringify({playlist_index: index, music_index: compIndex})
    }).then((response) => response.json()).then((data) => {
      this.setData(data);
    });
  }

  removeComposition(index, compIndex){
    fetch('/remove_composition', {
      method: 'POST', 
      cache: 'no-cache',
      body: JSON.stringify({playlist_index: index, music_index: compIndex})
    }).then((response) => response.json()).then((data) => {
      this.setData(data);
      this.props.updater();
    });
  }

  openDialog(){
    let name = prompt("Введите название плейлиста");
    if(name == undefined || name == '')
      return;
    fetch('/create_playlist', {
      method: 'POST',
      cache: 'no-cache',
      body: JSON.stringify({name: name})
    }).then((response) => response.json()).then((data) => {
      this.setData(data);
    });
  }

  render(){
    return (
      <div>
        <List
          sx={{ width: '36%', bgcolor: 'background.paper'}}
          component="nav"
          aria-labelledby="nested-list-subheader"
          subheader={
            <ListSubheader component="div" id="nested-list-subheader">
              Доступные плейлисты:
            </ListSubheader>
          }
        >
          {this.state.playlists.map((data, index) => (
            <ListItem sx={{flexDirection: 'column'}}>
              <Box sx={{display: 'flex', justifyContent:'space-between', width: '100%', alignItems: 'center', flexWrap: 'nowrap'}}>
                <Box sx={{whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden'}}>
                  {data.name}
                </Box>
                <Box>
                  <AddCompositionButton onClick={this.addComposition} index={index}></AddCompositionButton>
                  <DeletePlaylist onClick={this.deletePlaylist} index={index}></DeletePlaylist>
                </Box>
              </Box>
              <List sx={{width: '100%'}}>
                {data.compositions.map((compName, compIndex) => (
                  <ListItem sx={{display: 'flex', justifyContent:'space-between'}}>
                    <Box sx={{whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden'}}>
                      {compName}
                    </Box>
                    <Box>
                      <PlayComposition onClick={this.playComposition} index={index} compIndex={compIndex}></PlayComposition>
                      <PushBack onClick={this.pushBack} index={index} compIndex={compIndex}></PushBack>
                      <PushForward onClick={this.pushForward} index={index} compIndex={compIndex}></PushForward>
                      <RemoveComposition onClick={this.removeComposition} index={index} compIndex={compIndex}></RemoveComposition>
                    </Box>
                  </ListItem>
                ))}
              </List>
            </ListItem>))}
          <ListItem sx={{display: 'flex', justifyContent:'center'}}>
            <IconButton onClick={this.openDialog}>
              <ControlPointIcon />
            </IconButton>
          </ListItem>
        </List>
        <Dialog open={this.state.dialogOpened}>
          <DialogTitle>Выберите композицию для добавления в плейлист</DialogTitle>
          <List>
            {this.state.music.map((name, index) => (
              <AddMusicListButton name={name} index={index} dialogCallback={this.dialogCallback}></AddMusicListButton>
            ))}
          </List>
      </Dialog>
      </div>
    );
  }
}

class Player extends React.Component{
  constructor(props){
    super(props);
    this.state = {src: "", paused: true, name: ' '};
    this.audio = React.createRef();
    this.progress = React.createRef();
    this.onAudioEnded = this.onAudioEnded.bind(this);
    this.goPrevious = this.goPrevious.bind(this);
    this.goNext = this.goNext.bind(this);
  }

  componentDidMount(){
    this.audio.current.volume = 0.3;
    document.addEventListener('keydown', (e) => {
      if(e.key == 'ArrowRight'){
        this.audio.current.currentTime = Math.min(this.audio.current.duration, this.audio.current.currentTime + 5);
        this.updateProgress();
      }
      else if(e.key == 'ArrowLeft'){
        this.audio.current.currentTime = Math.max(0, this.audio.current.currentTime - 5);
        this.updateProgress();
      }
    })
  }

  updateSelf(){
    fetch('/get_music_data', {
      method: 'POST',
      cache: 'no-cache',
    }).then((response) => response.json()).then((data) => {
      if(data.state == 'ok'){
        this.setState({src: data.data, paused: this.state.paused, name: data.name, progress: 0});
      }
      else{
        this.setState({src: '', paused: this.state.paused, name: ' ', progress: 0});
      }
    });
  }

  updateProgress(){
    let duration = this.audio.current.duration;
    if(duration == NaN){
      duration = Infinity;
    }
    this.setState({...this.state, progress: this.audio.current.currentTime / duration * 100});
  }

  onAudioEnded(){
    fetch('/play_next', {
      method: 'POST',
      cache: 'no-cache',
    }).then(() => {
      this.updateSelf();
    }).then(() => {
      this.props.updater();
    });
  }

  goPrevious(){
    if(this.state.progress > 15){
      this.audio.current.currentTime = 0;
      this.updateProgress();
    }
    else{
      fetch('/play_previous', {
        method: 'POST',
        cache: 'no-cache'
      }).then(() => {
        this.updateSelf();
      }).then(() =>{
        this.props.updater();
      });
    }
  }

  goNext(){
    fetch('/play_next', {
      method: 'POST',
      cache: 'no-cache'
    }).then(() => {
      this.updateSelf();
    }).then(() =>{
      this.props.updater();
    });
  }

  render(){
    return (<div style={{position: 'fixed', top: '0', bottom: '0', right: '0', width: '64%'}}>
      <audio ref={this.audio} src={this.state.src} type="audio/mp3" autoPlay={!this.state.paused} onEnded={this.onAudioEnded} onTimeUpdate={() => {this.updateProgress();}}>
      </audio>
      <Container>
        <MusicNoteIcon color='action' sx={{
          width: '40vh', 
          height: '40vh'
        }}>
        </MusicNoteIcon>
      </Container>
      <Container>
        <h1>{this.state.name}</h1>
        <LinearProgress variant="determinate" value={this.state.progress} ref={this.progress}/>
      </Container>
      <Container sx={{display: 'flex', justifyContent: 'space-around', marginTop: '5vh'}}>
        <IconButton>
          <SkipPreviousRoundedIcon sx={{width: '20vh', height: '20vh'}} onClick={this.goPrevious}/>
        </IconButton>
        <IconButton>
          {this.state.paused ? <PlayArrowRoundedIcon sx={{width: '20vh', height: '20vh'}} onClick={() => {
            this.setState({...this.state, paused: false});
            this.audio.current.play();
          }}/>:
          <PauseRoundedIcon sx={{width: '20vh', height: '20vh'}} onClick={() => {
            this.setState({...this.state, paused: true});
            this.audio.current.pause();
          }}>
          </PauseRoundedIcon>}
        </IconButton>
        <IconButton>
          <SkipNextRoundedIcon sx={{width: '20vh', height: '20vh'}} onClick={this.goNext}/>
        </IconButton>
      </Container>
    </div>);
  }
}

class App extends React.Component{
  constructor(props){
    super(props);
    this.player = React.createRef();
    this.playlists = React.createRef();
  }

  render(){
    return (
      <div className="App">
        <PlayListList ref={this.playlists} updater={() =>{
          this.player.current.updateSelf();
        }}/>
        <Player ref={this.player} updater={() =>{
          this.player.current.updateSelf();
        }}/>
      </div>
      
    )
  }
}

export default App;
