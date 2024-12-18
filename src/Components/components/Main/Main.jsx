import React, { useContext, useEffect, useRef, useState } from "react";
import "./Main.css";
import { assets } from "src/assets/assets.js";
import { Context } from "src/context/Context.jsx";

const Main = () => {
    const {onSent, recentPrompt, showResult, loading, resultData, setInput, input} = useContext(Context);
    const resultRef = useRef(null);
    const [rows, setRows] = useState(1);

    useEffect(() => {
        const updateRows = () => {
            if (window.innerWidth <= 600) {
                setRows(2);
            } else {
                setRows(1);
            }
        };

        updateRows();
        window.addEventListener('resize', updateRows);
        return () => window.removeEventListener('resize', updateRows);
    }, []);

    useEffect(() => {
        if (resultRef.current) {
            resultRef.current.scrollTop = resultRef.current.scrollHeight;
        }
    }, [resultData]);

    return (
        <main className="main2">
            <nav className="nav">
                <p>SpeakSmart</p>
                <img src={assets.user_icon} alt=""/>
            </nav>
            <div className="main2-container">

                {!showResult
                    ? <>
                        <div className="greet">
                            <p><span>Hello, User</span></p>
                            <p>I am your virtual AI Speech Therapist</p>
                        </div>
                        <div className="cards">
                            <div className="card"
                                 onClick={() => setInput("Analyze my last months voice reports")}>
                                <p>Analyze the Voice reports of user</p>
                                <img src={assets.compass_icon} alt=""/>
                            </div>
                            <div className="card"
                                 onClick={() => setInput("What are some speech therapy techniques for adults?")}>
                                <p>Speech therapy techniques for adults</p>
                                <img src={assets.message_icon} alt=""/>
                            </div>
                            <div className="card"
                                 onClick={() => setInput("Brainstorm team bonding activities for our work retreat")}>
                                <p>Brainstorm team bonding activities for our work retreat</p>
                                <img src={assets.message_icon} alt=""/>
                            </div>
                            <div className="card" onClick={() => setInput("How can speech therapy help with stuttering?")}>
                                <p>How speech therapy can help with stuttering</p>
                                <img src={assets.code_icon} alt=""/>
                            </div>
                        </div>
                    </>
                    :
                    <div className='result' ref={resultRef}>
                        <div className="result-title">
                            <img src={assets.user_icon} alt=""/>
                            <p>{recentPrompt}</p>
                        </div>
                        <div className="result-data">
                            <img className="result-data-icon" src={assets.gemini_icon} alt=""/>
                            {loading ?
                                <div className='loader'>
                                    <hr/>
                                    <hr/>
                                    <hr/>
                                </div>
                                :
                                <p dangerouslySetInnerHTML={{__html: resultData}}></p>
                            }
                        </div>
                    </div>
                }
                <div className="main-bottom">
                    <div className="search-box">
                        <textarea rows={rows} onChange={(e) => setInput(e.target.value)}
                                  onKeyUp={(e) => {
                                      if (e.key === 'Enter') {
                                          onSent();
                                      }
                                  }}
                                  value={input}
                                  type="text"
                                  placeholder="Ask your question"
                        />
                        <div className="icon-container">
                            <button><img src={assets.gallery_icon} alt=""/></button>
                            <button><img src={assets.mic_icon} alt=""/></button>
                            <button type="submit" onClick={() => onSent()}><img src={assets.send_icon} alt=""/></button>
                        </div>
                    </div>
                    <p className="bottom-info">
                        Responses generated may not be accurate. Please do your own research. 
                        <a href="#">Privacy Policy</a>
                    </p>
                </div>
            </div>
        </main>
    );
}

export default Main;
