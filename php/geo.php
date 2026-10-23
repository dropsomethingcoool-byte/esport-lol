<?php
/**
 * geo.php — géolocalisation de l'IP du visiteur (règle de portail des CTA affiliés).
 *
 * Retourne un JSON { ip, city, region, country }.
 * Aucun tracking : le résultat n'est pas stocké côté serveur (uniquement
 * consulté par le JS pour décider d'afficher ou non les CTA affiliés).
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
header('Pragma: no-cache');

function client_ip() {
    $ip = '';
    if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $ip = trim(explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'])[0]);
    } elseif (!empty($_SERVER['HTTP_CF_CONNECTING_IP'])) {
        $ip = trim($_SERVER['HTTP_CF_CONNECTING_IP']);
    } elseif (!empty($_SERVER['REMOTE_ADDR'])) {
        $ip = trim($_SERVER['REMOTE_ADDR']);
    }
    return $ip;
}

function is_private_ip($ip) {
    return !$ip
        || $ip === '::1'
        || $ip === '127.0.0.1'
        || filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE) === false;
}

function http_get_json($url) {
    $ctx = stream_context_create(array(
        'http' => array(
            'timeout' => 4,
            'header' => "User-Agent: esport-lol-geo/1.0\r\nAccept: application/json\r\n",
        ),
        'ssl' => array('verify_peer' => true),
    ));
    $raw = @file_get_contents($url, false, $ctx);
    if ($raw === false) {
        return null;
    }
    $data = json_decode($raw, true);
    return is_array($data) ? $data : null;
}

$ip = client_ip();
$out = array('ip' => $ip, 'city' => null, 'region' => null, 'country' => null);

if (is_private_ip($ip)) {
    echo json_encode($out);
    exit;
}

// ipwho.is (HTTPS, sans clé) en priorité, ip-api.com en secours.
$d = http_get_json('https://ipwho.is/' . rawurlencode($ip) . '?lang=fr');
if (!$d || empty($d['success'])) {
    $d = http_get_json('http://ip-api.com/json/' . rawurlencode($ip) . '?fields=status,message,city,regionName,countryCode&lang=fr');
    if ($d && isset($d['status']) && $d['status'] === 'success') {
        $out['city']    = $d['city'] ?? null;
        $out['region']  = $d['regionName'] ?? null;
        $out['country'] = $d['countryCode'] ?? null;
    }
} else {
    $out['city']    = $d['city'] ?? null;
    $out['region']  = $d['region'] ?? null;
    $out['country'] = $d['country_code'] ?? null;
}

echo json_encode($out);
