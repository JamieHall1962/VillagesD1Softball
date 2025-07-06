// --- DEBUG LOGGING ---
console.log("JS loaded: 20250708");
alert('New JavaScript version 20250708 loaded!');
// D1 Softball Stats Application
// Replicates all Flask app functionality with zero compromises

// Global data storage
let playersData = [];
let seasonsData = [];
let teamsData = [];
let gamesData = [];
let battingStatsData = [];

// Utility functions
function nostripleadingzero(value) {
    try {
        return ('%.3f' % value).lstrip('0');
    } catch (e) {
        return value;
    }
}

function calculatePlayerStats(playerNumber) {
    const playerBatting = battingStatsData.filter(stat => stat.player_number === playerNumber);
    if (playerBatting.length === 0) return null;

    const totalPa = playerBatting.reduce((sum, stat) => sum + stat.pa, 0);
    const totalR = playerBatting.reduce((sum, stat) => sum + stat.r, 0);
    const totalH = playerBatting.reduce((sum, stat) => sum + stat.h, 0);
    const total2b = playerBatting.reduce((sum, stat) => sum + stat.d, 0);
    const total3b = playerBatting.reduce((sum, stat) => sum + stat.t, 0);
    const totalHr = playerBatting.reduce((sum, stat) => sum + stat.hr, 0);
    const totalBb = playerBatting.reduce((sum, stat) => sum + stat.bb, 0);
    const totalSf = playerBatting.reduce((sum, stat) => sum + stat.sf, 0);
    const totalOe = playerBatting.reduce((sum, stat) => sum + stat.oe, 0);
    const totalRbi = playerBatting.reduce((sum, stat) => sum + stat.rbi, 0);
    const total1b = totalH - total2b - total3b - totalHr;

    // Calculate at-bats
    const totalAb = totalPa - totalBb - totalSf;

    // Games played with U2 correction
    const uniqueGames = new Set(playerBatting.map(stat => `${stat.team_number}-${stat.game_number}`)).size;
    const totalU2 = playerBatting.reduce((sum, stat) => sum + stat.u2, 0);
    const gamesPlayed = uniqueGames + totalU2;

    // Averages
    const avg = totalAb > 0 ? totalH / totalAb : 0;
    const obp = totalPa > 0 ? (totalH + totalBb) / totalPa : 0;
    const slg = totalAb > 0 ? (totalH + total2b + 2*total3b + 3*totalHr) / totalAb : 0;

    return {
        games_played: gamesPlayed,
        pa: totalPa,
        ab: totalAb,
        r: totalR,
        h: totalH,
        '1b': total1b,
        '2b': total2b,
        '3b': total3b,
        hr: totalHr,
        rbi: totalRbi,
        bb: totalBb,
        sf: totalSf,
        oe: totalOe,
        tb: totalH + total2b + 2*total3b + 3*totalHr,
        avg: avg,
        slg: slg,
        obp: obp
    };
}

// Load all data
async function loadData() {
    try {
        // Determine the correct base path for data files
        const path = window.location.pathname;
        let basePath = '';
        
        if (path.includes('/player/') || path.includes('/season/')) {
            basePath = '../';
        }
        
        const [playersResponse, seasonsResponse, teamsResponse, gamesResponse, battingResponse] = await Promise.all([
            fetch(basePath + 'data/players.json'),
            fetch(basePath + 'data/seasons.json'),
            fetch(basePath + 'data/games.json'),
            fetch(basePath + 'data/teams.json'),
            fetch(basePath + 'data/batting_stats.json')
        ]);

        playersData = await playersResponse.json();
        seasonsData = await seasonsResponse.json();
        teamsData = await teamsResponse.json();
        gamesData = await gamesResponse.json();
        battingStatsData = await battingResponse.json();

        console.log('Data loaded successfully!');
        initializeApp();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// Initialize application based on current page
function initializeApp() {
    const path = window.location.pathname;
    
    if (path.includes('players.html') || path.endsWith('/')) {
        initializePlayersPage();
    } else if (path.includes('seasons.html')) {
        initializeSeasonsPage();
    } else if (path.includes('player/')) {
        initializePlayerDetailPage();
    } else if (path.includes('season/')) {
        initializeSeasonDetailPage();
    }
}

// Players page functionality
function initializePlayersPage() {
    if (!document.getElementById('playersTableBody')) return;
    
    renderPlayersTable();
    setupPlayersSorting();
    setupPlayersSearch();
}

function renderPlayersTable() {
    const tbody = document.getElementById('playersTableBody');
    tbody.innerHTML = '';
    console.log('renderPlayersTable called');
    console.log('playersData:', playersData);
    if (!Array.isArray(playersData) || playersData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="19" style="color:red;font-weight:bold;">No player data found or data format error. Check console for details.</td></tr>';
        console.error('No player data found or data format error:', playersData);
        return;
    }
    let renderedRows = 0;
    playersData.forEach((player, index) => {
        if (!player.id || !player.name) {
            console.error('Malformed player object:', player);
            return;
        }
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td><a href="player/${player.id}.html" class="player-link">${player.name}</a></td>
            <td>${player.games_played}</td>
            <td>${player.pa}</td>
            <td>${player.ab}</td>
            <td>${player.r}</td>
            <td>${player.h}</td>
            <td>${player['1b']}</td>
            <td>${player['2b']}</td>
            <td>${player['3b']}</td>
            <td>${player.hr}</td>
            <td>${player.rbi}</td>
            <td>${player.bb}</td>
            <td>${player.sf}</td>
            <td>${player.oe}</td>
            <td>${player.tb}</td>
            <td>${nostripleadingzero(player.avg)}</td>
            <td>${nostripleadingzero(player.slg)}</td>
            <td>${nostripleadingzero(player.obp)}</td>
        `;
        tbody.appendChild(row);
        renderedRows++;
    });
    console.log('Rendered rows:', renderedRows);
    if (renderedRows === 0) {
        tbody.innerHTML = '<tr><td colspan="19" style="color:red;font-weight:bold;">No valid player rows rendered. Check console for details.</td></tr>';
    }
}

function setupPlayersSorting() {
    // Implementation for sorting (same as Flask app)
    let currentSort = { column: -1, direction: 1 };
    
    window.sortTable = function(columnIndex) {
        const table = document.getElementById('playersTable');
        const tbody = table.getElementsByTagName('tbody')[0];
        const rows = Array.from(tbody.getElementsByTagName('tr'));
        
        if (currentSort.column === columnIndex) {
            currentSort.direction = -currentSort.direction;
        } else {
            currentSort.direction = 1;
        }
        currentSort.column = columnIndex;
        
        rows.sort(function(a, b) {
            const aVal = a.cells[columnIndex].textContent.trim();
            const bVal = b.cells[columnIndex].textContent.trim();
            
            const aNum = parseFloat(aVal.replace(/[^0-9.-]/g, ''));
            const bNum = parseFloat(bVal.replace(/[^0-9.-]/g, ''));
            
            if (!isNaN(aNum) && !isNaN(bNum)) {
                return (aNum - bNum) * currentSort.direction;
            } else {
                return aVal.localeCompare(bVal) * currentSort.direction;
            }
        });
        
        rows.forEach(function(row) {
            tbody.appendChild(row);
        });
        
        updateRankNumbers();
        updateSortIndicators(columnIndex, currentSort.direction);
    };
}

function setupPlayersSearch() {
    const searchInput = document.getElementById('playerSearch');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const filter = this.value.toLowerCase();
        const table = document.getElementById('playersTable');
        const trs = table.getElementsByTagName('tr');
        
        for (let i = 1; i < trs.length; i++) {
            const nameCell = trs[i].getElementsByTagName('td')[1];
            if (nameCell) {
                const name = nameCell.textContent || nameCell.innerText;
                trs[i].style.display = name.toLowerCase().indexOf(filter) > -1 ? '' : 'none';
            }
        }
    });
}

function updateRankNumbers() {
    const tbody = document.getElementById('playersTable').getElementsByTagName('tbody')[0];
    const rows = tbody.getElementsByTagName('tr');
    for (let i = 0; i < rows.length; i++) {
        const rankCell = rows[i].cells[0];
        if (rankCell) {
            rankCell.textContent = i + 1;
        }
    }
}

function updateSortIndicators(column, direction) {
    const headers = document.querySelectorAll('.players-table th');
    headers.forEach(function(header, index) {
        let indicator = header.querySelector('.sort-indicator');
        if (!indicator) {
            indicator = document.createElement('span');
            indicator.className = 'sort-indicator';
            header.appendChild(indicator);
        }
        
        if (index === column) {
            indicator.textContent = direction === 1 ? '▲' : '▼';
        } else {
            indicator.textContent = '';
        }
    });
}

// Seasons page functionality
function initializeSeasonsPage() {
    if (!document.getElementById('seasonsList')) return;
    
    renderSeasonsList();
}

function renderSeasonsList() {
    const container = document.getElementById('seasonsList');
    container.innerHTML = '';
    
    seasonsData.forEach(season => {
        const div = document.createElement('div');
        div.className = 'season-item';
        div.innerHTML = `<a href="season/${season.season_code}.html" class="season-link">${season.season_name}</a>`;
        container.appendChild(div);
    });
}

// Player detail page functionality
function initializePlayerDetailPage() {
    if (!document.getElementById('playerContent')) return;
    
    // Extract player ID from URL
    const path = window.location.pathname;
    const match = path.match(/\/player\/(\d+)\.html$/);
    if (match) {
        const playerId = parseInt(match[1]);
        renderPlayerDetail(playerId);
    }
}

// Season detail page functionality
function initializeSeasonDetailPage() {
    if (!document.getElementById('seasonContent')) return;
    
    // Extract season code from URL
    const path = window.location.pathname;
    const match = path.match(/\/season\/([^.]+)\.html$/);
    if (match) {
        const seasonCode = match[1];
        renderSeasonDetail(seasonCode);
    }
}

function renderPlayerDetail(playerId) {
    const player = playersData.find(p => p.id === playerId);
    if (!player) {
        document.getElementById('playerContent').innerHTML = '<p>Player not found.</p>';
        return;
    }
    
    // Calculate season breakdown
    const seasonBreakdown = calculatePlayerSeasonBreakdown(playerId);
    
    // Render career stats grid
    const statsGrid = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${player.games_played}</div>
                <div class="stat-label">Games</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.pa}</div>
                <div class="stat-label">PA</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.ab}</div>
                <div class="stat-label">AB</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.h}</div>
                <div class="stat-label">H</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.r}</div>
                <div class="stat-label">R</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.rbi}</div>
                <div class="stat-label">RBI</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player['2b']}</div>
                <div class="stat-label">2B</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player['3b']}</div>
                <div class="stat-label">3B</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.hr}</div>
                <div class="stat-label">HR</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.bb}</div>
                <div class="stat-label">BB</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${nostripleadingzero(player.avg)}</div>
                <div class="stat-label">AVG</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${nostripleadingzero(player.obp)}</div>
                <div class="stat-label">OBP</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${nostripleadingzero(player.slg)}</div>
                <div class="stat-label">SLG</div>
            </div>
        </div>
    `;
    
    // Render season breakdown table
    const seasonTable = `
        <h2>${seasonBreakdown.length} Seasons</h2>
        <div class="table-container">
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Season</th>
                        <th>Team</th>
                        <th>G</th>
                        <th>PA</th>
                        <th>AB</th>
                        <th>H</th>
                        <th>R</th>
                        <th>RBI</th>
                        <th>2B</th>
                        <th>3B</th>
                        <th>HR</th>
                        <th>BB</th>
                        <th>AVG</th>
                        <th>OBP</th>
                        <th>SLG</th>
                    </tr>
                </thead>
                <tbody>
                    ${seasonBreakdown.map(season => `
                        <tr>
                            <td><a href="../season/${season.season_code}.html" class="season-link">${season.season_name}</a></td>
                            <td>${season.team_name}</td>
                            <td>${season.games_played}</td>
                            <td>${season.pa}</td>
                            <td>${season.ab}</td>
                            <td>${season.h}</td>
                            <td>${season.r}</td>
                            <td>${season.rbi}</td>
                            <td>${season['2b']}</td>
                            <td>${season['3b']}</td>
                            <td>${season.hr}</td>
                            <td>${season.bb}</td>
                            <td>${nostripleadingzero(season.avg)}</td>
                            <td>${nostripleadingzero(season.obp)}</td>
                            <td>${nostripleadingzero(season.slg)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    document.getElementById('playerContent').innerHTML = statsGrid + seasonTable;
}

function calculatePlayerSeasonBreakdown(playerId) {
    const playerStats = battingStatsData.filter(stat => stat.player_number === playerId);
    if (playerStats.length === 0) return [];
    
    // Group by team to get season information
    const teamStats = {};
    playerStats.forEach(stat => {
        if (!teamStats[stat.team_number]) {
            teamStats[stat.team_number] = [];
        }
        teamStats[stat.team_number].push(stat);
    });
    
    const breakdown = [];
    
    Object.keys(teamStats).forEach(teamNumber => {
        const teamStat = teamStats[teamNumber];
        const totalPa = teamStat.reduce((sum, stat) => sum + stat.pa, 0);
        const totalR = teamStat.reduce((sum, stat) => sum + stat.r, 0);
        const totalH = teamStat.reduce((sum, stat) => sum + stat.h, 0);
        const total2b = teamStat.reduce((sum, stat) => sum + stat.d, 0);
        const total3b = teamStat.reduce((sum, stat) => sum + stat.t, 0);
        const totalHr = teamStat.reduce((sum, stat) => sum + stat.hr, 0);
        const totalBb = teamStat.reduce((sum, stat) => sum + stat.bb, 0);
        const totalRbi = teamStat.reduce((sum, stat) => sum + stat.rbi, 0);
        const totalSf = teamStat.reduce((sum, stat) => sum + stat.sf, 0);
        const totalOe = teamStat.reduce((sum, stat) => sum + stat.oe, 0);
        
        // Calculate at-bats
        const totalAb = totalPa - totalBb - totalSf;
        
        // Games played with U2 correction
        const uniqueGames = new Set(teamStat.map(stat => `${stat.team_number}-${stat.game_number}`)).size;
        const totalU2 = teamStat.reduce((sum, stat) => sum + stat.u2, 0);
        const gamesPlayed = uniqueGames + totalU2;
        
        // Averages
        const avg = totalAb > 0 ? totalH / totalAb : 0;
        const obp = totalPa > 0 ? (totalH + totalBb) / totalPa : 0;
        const slg = totalAb > 0 ? (totalH + total2b + 2*total3b + 3*totalHr) / totalAb : 0;
        
        // Find team name
        const team = teamsData.find(t => t.team_number === parseInt(teamNumber));
        const teamName = team ? team.team_name : `Team ${teamNumber}`;
        
        // Extract season code from team name
        const seasonMatch = teamName.match(/\s([WSF]\d{2})$/);
        const seasonCode = seasonMatch ? seasonMatch[1] : 'Unknown';
        
        // Find season name
        const season = seasonsData.find(s => s.season_code === seasonCode);
        const seasonName = season ? season.season_name : seasonCode;
        
        breakdown.push({
            season_code: seasonCode,
            season_name: seasonName,
            team_name: teamName,
            games_played: gamesPlayed,
            pa: totalPa,
            ab: totalAb,
            h: totalH,
            r: totalR,
            rbi: totalRbi,
            '2b': total2b,
            '3b': total3b,
            hr: totalHr,
            bb: totalBb,
            avg: avg,
            obp: obp,
            slg: slg
        });
    });
    
    // Sort by season (Winter=1, Summer=2, Fall=3)
    breakdown.sort((a, b) => {
        const aCode = a.season_code;
        const bCode = b.season_code;
        
        const aYear = parseInt(aCode.slice(1));
        const bYear = parseInt(bCode.slice(1));
        const aSeason = aCode[0];
        const bSeason = bCode[0];
        
        const seasonOrder = { 'W': 1, 'S': 2, 'F': 3 };
        
        if (aYear !== bYear) return bYear - aYear; // Newest first
        return seasonOrder[aSeason] - seasonOrder[bSeason];
    });
    
    return breakdown;
}

// Season detail page functionality
function renderSeasonDetail(seasonCode) {
    const season = seasonsData.find(s => s.season_code === seasonCode);
    if (!season) {
        document.getElementById('seasonContent').innerHTML = '<p>Season not found.</p>';
        return;
    }
    
    // Calculate standings for this season
    const standings = calculateSeasonStandings(seasonCode);
    
    // Render standings
    let standingsHtml = '';
    
    if (standings.divisions && standings.divisions.length > 1) {
        // Multiple divisions
        standings.divisions.forEach(division => {
            standingsHtml += `
                <div class="division-section">
                    <div class="division-title">${division.name}</div>
                    <div class="table-container">
                        <table class="table table-striped table-hover">
                            <thead>
                                <tr>
                                    <th>Rank</th>
                                    <th>Team</th>
                                    <th>W</th>
                                    <th>L</th>
                                    <th>PCT</th>
                                    <th>GB</th>
                                    <th>R</th>
                                    <th>RA</th>
                                    <th>R/G</th>
                                    <th>RA/G</th>
                                    <th>BA</th>
                                    <th>OBP</th>
                                    <th>SLG</th>
                                    <th>HR</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${division.teams.map((team, index) => `
                                    <tr>
                                        <td>${index + 1}</td>
                                        <td><a href="../team/${team.team_number}.html" class="team-link">${team.team_name}</a></td>
                                        <td>${team.wins}</td>
                                        <td>${team.losses}</td>
                                        <td>${nostripleadingzero(team.win_pct)}</td>
                                        <td>${team.games_back}</td>
                                        <td>${team.runs}</td>
                                        <td>${team.runs_allowed}</td>
                                        <td>${nostripleadingzero(team.runs_per_game)}</td>
                                        <td>${nostripleadingzero(team.runs_allowed_per_game)}</td>
                                        <td>${nostripleadingzero(team.team_avg)}</td>
                                        <td>${nostripleadingzero(team.team_obp)}</td>
                                        <td>${nostripleadingzero(team.team_slg)}</td>
                                        <td>${team.team_hr}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
        });
    } else {
        // Single division
        const teams = standings.divisions[0].teams;
        standingsHtml = `
            <div class="table-container">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Team</th>
                            <th>W</th>
                            <th>L</th>
                            <th>PCT</th>
                            <th>GB</th>
                            <th>R</th>
                            <th>RA</th>
                            <th>R/G</th>
                            <th>RA/G</th>
                            <th>BA</th>
                            <th>OBP</th>
                            <th>SLG</th>
                            <th>HR</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${teams.map((team, index) => `
                            <tr>
                                <td>${index + 1}</td>
                                <td><a href="../team/${team.team_number}.html" class="team-link">${team.team_name}</a></td>
                                <td>${team.wins}</td>
                                <td>${team.losses}</td>
                                <td>${nostripleadingzero(team.win_pct)}</td>
                                <td>${team.games_back}</td>
                                <td>${team.runs}</td>
                                <td>${team.runs_allowed}</td>
                                <td>${nostripleadingzero(team.runs_per_game)}</td>
                                <td>${nostripleadingzero(team.runs_allowed_per_game)}</td>
                                <td>${nostripleadingzero(team.team_avg)}</td>
                                <td>${nostripleadingzero(team.team_obp)}</td>
                                <td>${nostripleadingzero(team.team_slg)}</td>
                                <td>${team.team_hr}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }
    
    // Add note for combined seasons if needed
    if (['S15', 'S16', 'S17'].includes(seasonCode)) {
        standingsHtml = `
            <div class="note-box">
                <strong>Note:</strong> This season combined D1 and D2 divisions. Only D1 player statistics were recorded.
            </div>
        ` + standingsHtml;
    }
    
    document.getElementById('seasonContent').innerHTML = standingsHtml;
}

function calculateSeasonStandings(seasonCode) {
    // Find teams for this season
    const seasonTeams = teamsData.filter(team => {
        const seasonMatch = team.team_name.match(/\s([WSF]\d{2})$/);
        return seasonMatch && seasonMatch[1] === seasonCode;
    });
    
    if (seasonTeams.length === 0) {
        return {
            divisions: [{
                name: 'Division',
                teams: []
            }]
        };
    }
    
    // Check for divisions (teams with parentheses in names)
    const divisions = {};
    seasonTeams.forEach(team => {
        const divisionMatch = team.team_name.match(/\(([^)]+)\)/);
        const divisionName = divisionMatch ? divisionMatch[1] : 'Division';
        
        if (!divisions[divisionName]) {
            divisions[divisionName] = [];
        }
        divisions[divisionName].push(team);
    });
    
    // Calculate standings for each division
    const divisionStandings = [];
    
    Object.keys(divisions).forEach(divisionName => {
        const teams = divisions[divisionName];
        const teamStandings = [];
        
        teams.forEach(team => {
            // Get games for this team in this season
            const teamGames = gamesData.filter(game => game.team_number === team.team_number);
            
            let wins = 0;
            let losses = 0;
            let runs = 0;
            let runsAllowed = 0;
            
            teamGames.forEach(game => {
                runs += game.runs;
                runsAllowed += game.opp_runs;
                
                if (game.runs > game.opp_runs) {
                    wins++;
                } else if (game.runs < game.opp_runs) {
                    losses++;
                }
            });
            
            // Calculate team batting stats
            const teamBatting = battingStatsData.filter(stat => stat.team_number === team.team_number);
            const totalPa = teamBatting.reduce((sum, stat) => sum + stat.pa, 0);
            const totalH = teamBatting.reduce((sum, stat) => sum + stat.h, 0);
            const total2b = teamBatting.reduce((sum, stat) => sum + stat.d, 0);
            const total3b = teamBatting.reduce((sum, stat) => sum + stat.t, 0);
            const totalHr = teamBatting.reduce((sum, stat) => sum + stat.hr, 0);
            const totalBb = teamBatting.reduce((sum, stat) => sum + stat.bb, 0);
            const totalSf = teamBatting.reduce((sum, stat) => sum + stat.sf, 0);
            
            const totalAb = totalPa - totalBb - totalSf;
            const teamAvg = totalAb > 0 ? totalH / totalAb : 0;
            const teamObp = totalPa > 0 ? (totalH + totalBb) / totalPa : 0;
            const teamSlg = totalAb > 0 ? (totalH + total2b + 2*total3b + 3*totalHr) / totalAb : 0;
            
            const winPct = (wins + losses) > 0 ? wins / (wins + losses) : 0;
            const gamesPlayed = wins + losses;
            const runsPerGame = gamesPlayed > 0 ? runs / gamesPlayed : 0;
            const runsAllowedPerGame = gamesPlayed > 0 ? runsAllowed / gamesPlayed : 0;
            
            teamStandings.push({
                team_number: team.team_number,
                team_name: team.team_name,
                wins: wins,
                losses: losses,
                win_pct: winPct,
                games_back: 0, // Will be calculated below
                runs: runs,
                runs_allowed: runsAllowed,
                runs_per_game: runsPerGame,
                runs_allowed_per_game: runsAllowedPerGame,
                team_avg: teamAvg,
                team_obp: teamObp,
                team_slg: teamSlg,
                team_hr: totalHr
            });
        });
        
        // Sort by winning percentage
        teamStandings.sort((a, b) => b.win_pct - a.win_pct);
        
        // Calculate games back
        if (teamStandings.length > 0) {
            const firstPlaceWins = teamStandings[0].wins;
            const firstPlaceLosses = teamStandings[0].losses;
            
            teamStandings.forEach((team, index) => {
                if (index === 0) {
                    team.games_back = 0;
                } else {
                    const gamesBack = ((firstPlaceWins - team.wins) + (team.losses - firstPlaceLosses)) / 2;
                    team.games_back = gamesBack;
                }
            });
        }
        
        divisionStandings.push({
            name: divisionName,
            teams: teamStandings
        });
    });
    
    return {
        divisions: divisionStandings
    };
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', loadData);

// Export functions for use in other scripts
window.D1Stats = {
    loadData,
    calculatePlayerStats,
    nostripleadingzero
};
