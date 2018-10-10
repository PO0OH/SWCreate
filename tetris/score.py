class ScoreManager:


    s_linesPerLevel = 10
    s_initialSpeed  = 500 # Milliseconds inbetween tetrimino gravity updates
    s_levelIncreaseSpeed = 75
    s_speedClamp = 100
    s_lines = 0
    s_speed = s_initialSpeed


    def addLine():
        ScoreManager.s_lines = ScoreManager.s_lines + 1
        if ScoreManager.s_lines % ScoreManager.s_linesPerLevel == 0:
            ScoreManager.s_speed = ScoreManager.s_speed - ScoreManager.s_levelIncreaseSpeed
            if ScoreManager.s_speed < ScoreManager.s_speedClamp:
                ScoreManager.s_speed = ScoreManager.s_speedClamp
        return


    def getLevel():
        return int( ScoreManager.s_lines / ScoreManager.s_linesPerLevel )
