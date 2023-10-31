import React, { useEffect, useRef, useState } from "react";
import Logo from "./Logo";
import styles from "./GamePage.module.css";
import OthelloBoard from "./OthelloBoard";
import { useCallback } from "react";

function GamePage() {
  const canvasRef = useRef(null);
  const [started, setStarted] = useState(0);
  const [ws, setWs] = useState(null);
  const [userId, setUserId] = useState(localStorage.getItem("userid"));
  const [guestId, setGuestId] = useState(localStorage.getItem("guestid"));
  const [whiteCount, setWhiteCount] = useState(2);
  const [blackCount, setBlackCount] = useState(2);

  /* Callback function that will be called by OthelloBoard. 
  Returns the current count of the white and black pieces */
  const countChangeHandler = useCallback((newWhite, newBlack) => {
    setWhiteCount(newWhite);
    setBlackCount(newBlack);
  }, []);

  /* Once clicked, {started} will be modified, 
    and useEffect() in OthelloBoard.js will be re-rendered. */
  const handleConnectClick = () => {
    let gameId;
    if (!userId) {
      if (!guestId) {
        setGuestId(crypto.randomUUID());
        localStorage.setItem("guestid", guestId);
      } else {
        gameId = guestId;
      }
    } else {
      gameId = userId;
    }

    setStarted(1);

    const newWs = new WebSocket(
      "ws://localhost:8000/othelloml_api/ws/pvp-session/" + gameId
    );
    setWs(newWs);

    newWs.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      console.log(msg);
    };

    newWs.onopen = (event) => {
      newWs.send("d");
    };

    newWs.onclose = (event) => {
      alert("Connection lost! This might be intentional.");
    };

    newWs.onerror = (event) => {
      alert("Error occurred!");
    };
  };

  return (
    <div>
      <div className="container py-5">
        <div className={styles.header}>
          <Logo alt="Logo" className={styles.logo} />
          <h1 style={{ fontSize: "60px" }}>Othello ML</h1>
        </div>
        <div className={styles.main}>
          <div className={styles.nav}>
            <a href="#" id={styles.home}>
              Home
            </a>
            <a href="#" className={styles.button} id={styles.newGameBtn}>
              Game
            </a>
            <a href="#">Rules</a>
            <a href="#">About</a>
            <input type="text" placeholder="search player" id={styles.search} />
          </div>
          <div className={styles.game}>
            <div className="text-center ms-3">
              {/*
                props for OthelloBoard.js()
                started: will be set to 1 once the handleConnectClick() is called (users clicks on connection button)
                onDataChange: callback function that will update the latest piece counts
                */}
              <OthelloBoard
                started={started}
                onDataChange={countChangeHandler}
                whiteCount={whiteCount}
                blackCount={blackCount}
              />
            </div>
            <div className={styles.gameText}>
              <div>
                <div className={styles.count}>
                  <h2 id={styles.numWhite}>White: {whiteCount}</h2>
                  <h2 id={styles.numBlack}>Black: {blackCount}</h2>
                </div>
              </div>
              <div>
                <button id={styles.connectBtn} onClick={handleConnectClick}>
                  Connect
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default GamePage;
