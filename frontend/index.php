<?php
include 'config.php';

$keyword = isset($_GET['keyword']) ? $_GET['keyword'] : '';
$pendidikan = isset($_GET['pendidikan']) ? $_GET['pendidikan'] : '';
$lokasi = isset($_GET['lokasi']) ? $_GET['lokasi'] : '';
$portal = isset($_GET['portal']) ? $_GET['portal'] : '';

$query = "SELECT * FROM jobs WHERE 1=1";

if (!empty($keyword)) {
    $keyword_safe = mysqli_real_escape_string($conn, $keyword);
    $query .= " AND (
        judul_posisi LIKE '%$keyword_safe%' OR 
        nama_perusahaan LIKE '%$keyword_safe%' OR 
        lokasi LIKE '%$keyword_safe%' OR
        portal_sumber LIKE '%$keyword_safe%'
    )";
}

if (!empty($pendidikan)) {
    $pendidikan_safe = mysqli_real_escape_string($conn, $pendidikan);
    $query .= " AND pendidikan LIKE '%$pendidikan_safe%'";
}

if (!empty($lokasi)) {
    $lokasi_safe = mysqli_real_escape_string($conn, $lokasi);
    $query .= " AND lokasi LIKE '%$lokasi_safe%'";
}

if (!empty($portal)) {
    $portal_safe = mysqli_real_escape_string($conn, $portal);
    $query .= " AND portal_sumber LIKE '%$portal_safe%'";
}

$query .= " ORDER BY judul_posisi ASC";
$result = mysqli_query($conn, $query);
$total = mysqli_num_rows($result);
?>

<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Job Aggregator</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

<header class="navbar">
    <div class="logo"><span>Job</span> Aggregator</div>
    <nav>
        <a href="index.php" class="active">Beranda</a>
        <a href="#">Lowongan</a>
        <a href="#">Tentang</a>
        <a href="#">Kontak</a>
    </nav>
</header>

<main class="container">

    <section class="hero-search">
        <form method="GET" class="search-form">
            <input type="text" name="keyword" placeholder="Cari posisi, perusahaan, atau kata kunci..."
                   value="<?= htmlspecialchars($keyword); ?>">
            <input type="text" name="lokasi" placeholder="Lokasi, contoh: Jakarta, Bandung..."
                   value="<?= htmlspecialchars($lokasi); ?>">
            <button type="submit">Cari Lowongan</button>
        </form>
    </section>

    <section class="content">

        <aside class="sidebar">
            <h3>Filter Pencarian</h3>

            <form method="GET">
                <input type="hidden" name="keyword" value="<?= htmlspecialchars($keyword); ?>">
                <input type="hidden" name="lokasi" value="<?= htmlspecialchars($lokasi); ?>">

                <div class="filter-group">
                    <h4>Pendidikan</h4>
                    <label><input type="radio" name="pendidikan" value="" <?= $pendidikan == '' ? 'checked' : ''; ?>> Semua Pendidikan</label>
                    <label><input type="radio" name="pendidikan" value="SMA" <?= $pendidikan == 'SMA' ? 'checked' : ''; ?>> SMA</label>
                    <label><input type="radio" name="pendidikan" value="SMK" <?= $pendidikan == 'SMK' ? 'checked' : ''; ?>> SMK</label>
                    <label><input type="radio" name="pendidikan" value="D3" <?= $pendidikan == 'D3' ? 'checked' : ''; ?>> D3</label>
                    <label><input type="radio" name="pendidikan" value="S1" <?= $pendidikan == 'S1' ? 'checked' : ''; ?>> S1 / Sarjana</label>
                </div>

                <div class="filter-group">
                    <h4>Sumber Portal</h4>
                    <label><input type="radio" name="portal" value="" <?= $portal == '' ? 'checked' : ''; ?>> Semua Portal</label>
                    <label><input type="radio" name="portal" value="Glints" <?= $portal == 'Glints' ? 'checked' : ''; ?>> Glints</label>
                    <label><input type="radio" name="portal" value="Jobstreet" <?= $portal == 'Jobstreet' ? 'checked' : ''; ?>> Jobstreet</label>
                </div>

                <div class="filter-group">
                    <h4>Jenis Pekerjaan</h4>
                    <label><input type="checkbox"> Full Time</label>
                    <label><input type="checkbox"> Part Time</label>
                    <label><input type="checkbox"> Internship</label>
                </div>

                <button class="btn-filter" type="submit">Terapkan Filter</button>
                <a href="index.php" class="btn-reset">Reset</a>
            </form>
        </aside>

        <section class="jobs">
            <div class="result-header">
                <p>Menampilkan <strong><?= $total; ?></strong> lowongan pekerjaan</p>
            </div>

            <?php if ($total > 0): ?>
                <?php while ($row = mysqli_fetch_assoc($result)): ?>
                    <div class="job-card">
                        <div class="company-logo">
                            <?= strtoupper(substr($row['nama_perusahaan'], 0, 1)); ?>
                        </div>

                        <div class="job-info">
                            <h2><?= htmlspecialchars($row['judul_posisi']); ?></h2>
                            <p class="company"><?= htmlspecialchars($row['nama_perusahaan']); ?></p>

                            <div class="tags">
                                <span><?= htmlspecialchars($row['lokasi']); ?></span>
                                <span><?= !empty($row['pendidikan']) ? htmlspecialchars($row['pendidikan']) : 'Umum'; ?></span>
                                <span><?= htmlspecialchars($row['portal_sumber']); ?></span>
                            </div>

                            <p class="description">
                                Kualifikasi dan deskripsi pekerjaan dapat dilihat secara lengkap melalui sumber lowongan asli.
                            </p>
                        </div>

                        <div class="job-action">
                            <p class="source"><?= htmlspecialchars($row['portal_sumber']); ?></p>
                            <a href="<?= htmlspecialchars($row['link_lowongan']); ?>" target="_blank">Lihat Detail</a>
                        </div>
                    </div>
                <?php endwhile; ?>
            <?php else: ?>
                <div class="empty">
                    <h3>Data lowongan tidak ditemukan</h3>
                    <p>Coba gunakan kata kunci atau filter lain.</p>
                </div>
            <?php endif; ?>
        </section>

    </section>
</main>

</body>
</html>