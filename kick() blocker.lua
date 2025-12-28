--block kick() request, idk why i make this
local TeleportService = game:GetService("TeleportService")
local Players = game:GetService("Players")

local player = Players.LocalPlayer
local placeId = game.PlaceId

local mt = getrawmetatable(game)
local oldNamecall = mt.__namecall
setreadonly(mt, false)

mt.__namecall = newcclosure(function(self, ...)
    local args = {...}
    local method = getnamecallmethod()

    if self == player and method == "Kick" then
        warn("[AutoRejoin] Kick detected! Attempting to teleport to a new server...")
        task.spawn(function()
            pcall(function()
                -- Tìm server khác
                local HttpService = game:GetService("HttpService")
                local function findNewServer()
                    local servers = HttpService:JSONDecode(game:HttpGet(
                        "https://roblox.com/games/"..placeId.."/servers/Public?sortOrder=Asc&limit=100"))
                    for _, server in pairs(servers.data) do
                        if server.playing < server.maxPlayers and server.id ~= game.JobId then
                            return server.id
                        end
                    end
                    return nil
                end

                local newServer = findNewServer()
                if newServer then
                    TeleportService:TeleportToPlaceInstance(placeId, newServer, player)
                else
                    TeleportService:Teleport(placeId, player)
                end
            end)
        end)
        return nil
    end

    return oldNamecall(self, unpack(args))
end)

setreadonly(mt, true)

warn("[AutoRejoin] Loaded. Will attempt to rejoin if kicked (nuh uh).")
